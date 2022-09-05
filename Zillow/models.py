from typing import Tuple
import pandas as pd
import numpy as np
from Zillow.types import County, Features as ft
from Zillow.metrics import measure_model

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

    def score(self, x: pd.DataFrame, y: pd.DataFrame) -> Tuple[float, float]:
        '''returns mae'''
        return measure_model(y, self.predict(x))[0]


def generate_predictions(features: pd.DataFrame, ventura_model, orange_model, los_angeles_model, general_model, month = None) -> Tuple[list[float], list[int]]:
    predictions = []
    errors_idx = []
    for index, row in features.iterrows():
        if row[ft.county_id.value] == County.VENTURA.value:
            predictions.append( ventura_model.predict(row) )
        elif row[ft.county_id.value] == County.ORANGE.value:
            predictions.append( orange_model.predict(row) )
        elif row[ft.county_id.value] == County.LOS_ANGELES.value:
            predictions.append( los_angeles_model.predict(row) )
        else:
            predictions.append( general_model.predict(row) )
            errors_idx.append( index )
    
    return predictions, errors_idx

