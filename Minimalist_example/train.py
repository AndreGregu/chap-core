import argparse

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


def train(csv_fn, model_fn):
    df = pd.read_csv(csv_fn)
    features = ['rainfall', 'mean_temperature']
    X = df[features]
    Y = df['disease_cases']
    Y = Y.fillna(0)  # set NaNs to zero (not a good solution, just for the example to work)
    model = LinearRegression()
    model.fit(X, Y)
    joblib.dump(model, model_fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a minimalist forecasting model.')

    parser.add_argument('csv_fn', type=str, help='Path to the CSV file containing input data.')
    parser.add_argument('model_fn', type=str, help='Path to save the trained model.')
    args = parser.parse_args()
    train(args.csv_fn, args.model_fn)


