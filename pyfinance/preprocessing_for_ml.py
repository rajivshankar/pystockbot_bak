# preprocessing_for_ml.py
from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import model_selection, neighbors, svm
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

hm_days = 7


def process_data_for_labels(ticker):
    df = pd.read_csv('./data/sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        future_price = df[ticker].shift(-i)
        current_price = df[ticker]
        df['{}_{}d'.format(ticker, i)] = (
            future_price - current_price) / current_price

    df.fillna(0, inplace=True)
    return tickers, df


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.025
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    ticker_args = [df['{}_{}d'.format(ticker, i)] for i in range(1, hm_days+1)]

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *ticker_args))

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df


def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X,
                                                                        y,
                                                                        test_size=0.25)

    # clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)

    print(f'Accuracy, {confidence: 0.2f}')

    predictions = clf.predict(X_test)

    print('Predicted spread: ', Counter(predictions))

    return confidence


do_ml('BAC')
