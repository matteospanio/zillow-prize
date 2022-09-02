from msilib.schema import Error
import pandas as pd
import numpy as np
from data import County

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
        lista = [self.prediction for _ in range(len(x))]
        return np.array(lista)


def generate_predictions(features: pd.DataFrame, model):
    for row in features.iterrows():
        if row.regionidcounty == County.VENTURA:
            pass
        elif row.regionidcounty == County.ORANGE:
            pass
        elif row.regionidcounty == County.LOS_ANGELES:
            pass
        else: raise Exception('invalid county code')