from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from datetime import datetime
from constants import *
from user_key import data_key
from utils import get_dates_in_range
import numpy as np
import pandas as pd
import database as db
import pickle


def train(start_date, end_date):
    """
    Loads data from the month of start_date to the month of end_date (inclusive),
    trains a random forest classifier on that data, and saves the fitted model locally.

    :param start_date: datetime object, first day of first month of training data
    :param end_date: datetime object, first day of last month of training data
    """

    # get all dates for loading data
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    load_dates = get_dates_in_range(start_date, end_date)

    # load all training data
    train_dfs = []
    for date in load_dates:
        date_without_time = date.date()
        # load one month of train data from a GCP bucket as a pandas dataframe
        df = db.load(f'{data_key}-labelled-{date_without_time}')
        # don't include customers who got promos in the training data
        train_df = df[df['promo'] == 0]
        train_df = train_df.drop(['promo'], axis=1)
        train_dfs.append(train_df)
    train_df = pd.concat(train_dfs, axis=0)

    # split features from target
    y_train = train_df['churn']
    x_train = train_df.drop(['cust_id', 'date', 'churn', 'predicted_churn_probability'], axis=1)

    # insert DataContract creation code here #

    ##########################################

    x_train = x_train.fillna(0)  # ensure the model can still train if NaN values are present

    # train model
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    # save model
    pickle.dump(model, open("fitted_objects/model.pkl", "wb"))


def predict(inference_date):
    """
    Loads one month of inference data from a GCP bucket and runs inference using
    the locally saved model. The predictions are uploaded to GCP.

    :param inference_date: datetime object, the first day of the month to perform inference on
    """

    inference_date = inference_date.split(' ')[0]
    # load inference data from a GCP bucket as a pandas dataframe
    inference_df = db.load(f'{data_key}-inference-{inference_date}')
    # drop non-feature columns
    x_inference = inference_df.drop(['cust_id', 'date'], axis=1)

    # insert DataContract validation code here #

    ############################################

    x_inference = x_inference.fillna(0)

    # load model from local directory
    model = pickle.load(open("fitted_objects/model.pkl", "rb"))

    # run inference, and create a dataframe to store the predicted probabilities
    probs = model.predict_proba(x_inference)[:, 1]
    probs_df = pd.DataFrame(probs, columns=["predicted_churn_probability"])

    # save predictions to a GCP bucket
    db.save(f'{data_key}-predictions-{inference_date}', probs_df)


def eval(eval_date):
    """
    Loads one month of labelled data from a GCP bucket and calculates model performance
    on that month.

    :param eval_date: datetime object, the first day of the month to perform evaluation on
    """

    eval_date = eval_date.split(' ')[0]
    # load eval data from a GCP bucket as a pandas dataframe
    df = db.load(f'{data_key}-labelled-{eval_date}')

    # calculate accuracy, roc_auc, and confusion matrix
    targets = df["churn"]
    probs = df["predicted_churn_probability"]
    preds = [1 if prob > 0.5 else 0 for prob in probs]
    accuracy = accuracy_score(targets, preds)
    roc_auc = roc_auc_score(targets, probs)

    # calculate revenue
    n_active_custs = len(df[df.churn == 0])  # number of active customers in the evaluation month
    revenue = revenue_per_cust * n_active_custs

    # insert foundations metric tracking here #

    ###########################################

    return accuracy, roc_auc, n_active_custs, revenue