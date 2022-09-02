from typing import Tuple
import pandas as pd
import numpy as np
from Zillow.types import County, Features as ft

class Mean:
    '''
    A model shaped on sklearn ones to predict y with test mean.
    It works as basemodel, to see if adding parameters we get better results.
    '''
    
    prediction: float
    
    def __init__(self):
        self.prediction = 0.
    
    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        self.prediction = y.mean()
        
    def predict(self, x: pd.DataFrame):
        plist = [self.prediction for _ in range(len(x))]
        return np.array(plist)


def generate_predictions(features: pd.DataFrame, ventura_model, orange_model, los_angeles_model, general_model) -> Tuple[list[float], list[int]]:
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
