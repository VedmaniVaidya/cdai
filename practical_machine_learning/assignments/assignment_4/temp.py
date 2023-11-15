

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, RandomizedSearchCV, train_test_split
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import numpy as np


# Read the data from the csv files
df_train  = pd.read_csv('data/train.csv')
df_test   = pd.read_csv('data/test.csv')
df_train = df_train.drop(['id'], axis=1)
df_test = df_test.drop(['id'], axis=1)


X = df_train.drop(['smoking'], axis=1)
y = df_train['smoking']


#split the data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#load all the saved models from checpoints folder abd create a dictionary of models with their names
models = {
    'gs_xgbm_model': joblib.load('checkpoints/gs_xgbm_model.pkl'),
    'rs_xgb_model': joblib.load('checkpoints/rs_xgb_model.pkl'),
    'gs_lgbm_model': joblib.load('checkpoints/gs_lgbm_model.pkl'),
    # 'gs_catboost_model': joblib.load('checkpoints/gs_catboost_model.pkl')
}

#now using the models predict the probabilities of the test data and calulate roc_auc_score
predictions = {}
for model_name, model in models.items():
    predictions[model_name] = model.predict_proba(X_test)[:, 1]
    print(f'{model_name} roc_auc_score: {roc_auc_score(y_test, predictions[model_name])}')