from typing import Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import RFE

from Zillow.types import County, Features as ft

class BaseModel:
    '''
    A model shaped on sklearn ones to predict y with test mean or median.
    It works as basemodel, to see if adding parameters we get better results.
    '''
    
    _method: str
    _prediction: float
    
    def __init__(self, method: str = 'mean'):
        self._prediction = 0.
        self._method = method
    
    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        if self._method == 'mean':
            self._prediction = y.mean()
        elif self._method == 'median':
            self._prediction = y.median()
        
    def predict(self, x: pd.DataFrame, input_single_row: bool = False) -> np.ndarray:
        if input_single_row:
            return self._prediction
        return np.full(x.shape[0], self._prediction)

    # next methods are here just to respect sklearn models interface
    def get_params(self, deep: bool = True):
        return {}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self


def select_linear_regression_features(x: pd.DataFrame, y: pd.DataFrame, model: LinearRegression, scale: bool = False, plot: bool = False, cv: int = 5):
    '''
    Evaluate best parameters for linear regression model.
    '''
    x_scaled = x
    scaler = MinMaxScaler()

    if scale:
        x_scaled = scaler.fit_transform(x)
        x_scaled = pd.DataFrame(x_scaled, columns=x.columns)
    
    rfe = RFE(estimator=model, n_features_to_select=1)

    rfe.fit(x_scaled, y)

    best_features = np.array(x.columns.to_list())[ np.argsort(rfe.ranking_)[::-1] ]

    mae = []

    for f in range(1,len(best_features)+1):
        scores = cross_val_score(model,
                                x_scaled.loc[:,best_features[:f]], y, 
                                cv=cv, scoring='neg_mean_absolute_error')
        mae += [-scores.mean()]

    if plot:
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(range(1,len(best_features)+1), mae, 'o-', label="MAE")
        ax.set_title("MAE on varying features")
        ax.set_xlabel("Number of Best features used")
        ax.grid()
        plt.show()

    return best_features


def make_predictions(
    df: pd.DataFrame,
    orange_model,
    ventura_model,
    la_model,
    model_all,
    month: str, 
    o_transformer,
    o_encoder,
    v_transformer,
    v_encoder,
    la_transformer,
    la_encoder,
    all_transformer,
    all_encoder,
    verbose: bool = False):
    df[ft.transaction_date.value] = month
    results = np.array([])

    for i, row in df.iterrows():
        if verbose:
            print(f'Predicting {i+1}/{len(df)}')
            print(f'parcelid: {row[ft.parcelid.value]}')

        if row[ft.county_id] == County.ORANGE.value:
            row_trans = o_transformer.transform(row)
            row_enc = o_encoder.transform(row_trans)
            np.append(results, orange_model.predict(row_enc))

        elif row[ft.county_id] == County.VENTURA.value:
            row_trans = v_transformer.transform(row)
            row_enc = v_encoder.transform(row_trans)
            np.append(results, ventura_model.predict(row_enc))

        elif row[ft.county_id] == County.LOS_ANGELES.value:
            row_trans = la_transformer.transform(row)
            row_enc = la_encoder.transform(row_trans)
            np.append(results, la_model.predict(row_enc))

        else:
            row_trans = all_transformer.transform(row)
            row_enc = all_encoder.transform(row_trans)
            np.append(results, model_all.predict(row_enc))
        
    return results

