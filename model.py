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
    # get all dates for loading data
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    load_dates = get_dates_in_range(start_date, end_date)

    # load train data
    train_dfs = []
    for date in load_dates:
        date_without_time = date.date()
        df = db.load(f'{data_key}-labelled-{date_without_time}')
        train_dfs.append(df)
    train_df = pd.concat(train_dfs, axis=0)

    # split features from target
    y_train = train_df['churn']
    x_train = train_df.drop(['cust_id', 'date', 'churn', 'predicted_churn_probability'], axis=1)

    # insert DataContract creation code here #

    ##########################################

    x_train = x_train.fillna(0)

    # train model
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    # save model
    pickle.dump(model, open("fitted_objects/model.pkl", "wb"))


def predict(inference_date):
    inference_date = inference_date.split(' ')[0]
    # load inference data
    inference_df = db.load(f'{data_key}-inference-{inference_date}')
    # drop non-feature columns
    x_train = inference_df.drop(['cust_id', 'date'], axis=1)

    # insert DataContract validation code here #

    ############################################

    x_train = x_train.fillna(0)

    # load model
    model = pickle.load(open("fitted_objects/model.pkl", "rb"))

    # run inference
    probs = model.predict_proba(x_train)[:, 1]
    probs_df = pd.DataFrame(probs, columns=["predicted_churn_probability"])

    # save predictions to data bucket (not necessary if API is exposed and returns preds)
    db.save(f'{data_key}-predictions-{inference_date}', probs_df)


def eval(eval_date):
    eval_date = eval_date.split(' ')[0]
    # load eval data
    df = db.load(f'{data_key}-labelled-{eval_date}')
    # log accuracy and roc_auc
    targets = df["churn"]
    probs = df["predicted_churn_probability"]
    preds = [1 if prob > 0.5 else 0 for prob in probs]
    accuracy = accuracy_score(targets, preds)
    roc_auc = roc_auc_score(targets, probs)
    confusion_mat = confusion_matrix(targets, preds)

    # revenue, costs, and profits calc
    n_promos = np.sum(preds)
    n_active_custs = len(df[df.churn == 0])
    revenue = revenue_per_cust * n_active_custs

    # insert foundations metric tracking here #

    ###########################################

    return preds, confusion_mat, accuracy, roc_auc, n_promos, n_active_custs, revenue

