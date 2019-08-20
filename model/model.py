from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import database as db
import pickle
# import foundations

def train(start_date, end_date):
    '''
    :param start_date: pandas date
    :param end_date: pandas date
    :return:
    '''
    # load train data
    end_date_without_time = end_date.date()
    train_df = db.load(f'labelled-{end_date_without_time}')
    train_df = train_df[train_df.date >= start_date]

    # split features from target
    y_train = train_df['churn']
    feature_cols = [col_name for col_name in train_df.columns if 'feat' in col_name]
    x_train = train_df[feature_cols]
    x_train = x_train.fillna(0)

    # train model
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # save model
    pickle.dump(model, open("model_package/model.pkl", "wb"))


def predict(inference_date):
    # load inference data
    inference_date_without_time = inference_date.date()
    inference_df = db.load(f'inference-{inference_date_without_time}')
    inference_df = inference_df[inference_df.date == inference_date]
    feature_cols = [col_name for col_name in inference_df.columns if 'feat' in col_name]
    x_train = inference_df[feature_cols].fillna(0)

    # load model
    model = pickle.load(open("model_package/model.pkl", "rb"))

    # run inference
    preds = model.predict(x_train)
    probs = model.predict_proba(x_train)[:,1]

    # return inference results
    inference_df['predicted_churn'] = preds
    inference_df['predicted_churn_probability'] = probs
    return inference_df


def eval(eval_date):
    # load eval data
    eval_date_without_time = eval_date.date()
    df = db.load(f'labelled-{eval_date_without_time}')
    df = df[df.date == eval_date]
    # log accuracy and roc_auc
    targets = df["churn"]
    preds = df["predicted_churn"]
    probs = df["predicted_churn_probability"]

    accuracy = accuracy_score(targets, preds)
    roc_auc = roc_auc_score(targets, probs)

    # revenue, costs, and profits calc
    revenue_per_cust = 300
    cost_per_promo = 1500
    n_promos = preds.sum()
    n_active_custs = len(df[df.churn == 0])
    revenue = revenue_per_cust * n_active_custs
    cost = cost_per_promo * n_promos
    profit = revenue - cost

    # foundations logging
    # foundations.log_metric("accuracy", accuracy)
    # foundations.log_metric("roc_auc", roc_auc)
    # foundations.log_metric("revenue", revenue)
    # foundations.log_metric("cost", cost)
    # foundations.log_metric("profit", profit)
    # foundations.log_metric("n_promos", n_promos)
    # foundations.log_metric("n_active_custs", n_active_custs)

    return accuracy, roc_auc, revenue, cost, profit, n_promos, n_active_custs
