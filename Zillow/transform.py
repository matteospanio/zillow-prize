import math
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

import Zillow.data as zd
from Zillow.types import County, Features as ft, MoreFeatures as mft

_droplist = {
    'common': [
        'Unnamed: 0',
        ft.parcel_id.value,
        ft.assessment_year.value,
        ft.transaction_date.value,
        ft.air_conditioning_type.value,
        ft.land_use_type.value,
        ft.county_id.value,
        ft.pool_has_spa.value,
        ft.pool_is_spa.value,
        ft.not_spa_pool.value,
        ft.pool_size.value,
        ft.pool_cnt.value,
        ft.has_fireplace.value,
        ft.fireplace_cnt.value,
        ft.fips.value,
        ft.architectural_style.value,
        ft.deck_type.value,
        ft.calculated_bath_nbr.value,
        ft.full_bath_cnt.value,
        ft.zip_id.value,
        ft.three_quarter_bath_cnt.value,
        ft.construction_material.value,
        ft.finished_and_unfinished_sqft.value,
        ft.total_area_sqft.value,
        ft.neighborhood_id.value,
        ft.allowed_land_use_description.value,
        ft.county_land_use_code.value,
        ft.city_id.value,
        ft.census_tract_and_block.value,
        ft.raw_census_tract_and_block.value,
    ],
    County.ORANGE: [
        ft.building_condition.value,
        ft.heating_system_type.value,
    ],
    County.VENTURA: [
        ft.building_condition.value,
        ft.finished_first_floor_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.patio_in_yard_sqft.value,
        ft.storage_building_in_yard_sqft.value,
        ft.heating_system_type.value,
    ],
    County.LOS_ANGELES: [
        ft.finished_first_floor_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.garage_car_cnt.value,
        ft.garage_sqft.value,
        ft.room_cnt.value,
        ft.patio_in_yard_sqft.value,
        ft.storage_building_in_yard_sqft.value,
        ft.heating_system_type.value,
    ],
    'remove_all': [
        ft.room_cnt.value,
        ft.garage_sqft.value,
        ft.garage_car_cnt.value,
        ft.patio_in_yard_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.finished_first_floor_sqft.value,
        ft.heating_system_type.value,
        ft.building_condition.value,
        ft.storage_building_in_yard_sqft.value,
    ]
}

# one hot encoding
_categorical_features = {
    'to transform': [
        mft.transaction_month.value,
        mft.transaction_week_day.value,
        mft.land_use_label.value,
        mft.county_name.value,
    ],
    'to drop': [
        mft.transaction_month.value,
        mft.transaction_week_day.value,
        mft.land_use_label.value,
        mft.county_name.value,
        'x0_April',
        'x0_August',
        'x0_January',
        'x0_July',
        'x0_June',
        'x0_March',
        'x0_May',
        'x0_September',
    ]
}

_nan_to_zero = {
    'common': [
        ft.has_unpaid_tax.value,
        ft.unpaid_tax_year.value,
        ft.floors_cnt.value,
        ft.has_fireplace.value,
        ft.fireplace_cnt.value,
        ft.has_spa.value,
        ft.pool_cnt.value,
        ft.structures_built_cnt.value,
    ],
    County.ORANGE: [
        ft.garage_car_cnt.value,
        ft.garage_sqft.value,
        ft.patio_in_yard_sqft.value,
        ft.storage_building_in_yard_sqft.value,
    ],
    County.VENTURA: [
        ft.garage_car_cnt.value,
        ft.garage_sqft.value,
    ],
    County.LOS_ANGELES: [
    ],
}

_nan_to_mean = {
    'common': [
    ft.year_built.value,
    ft.finished_living_area_sqft.value,
    ft.structure_tax_value_dollar.value,
    ft.tax_assessed.value,
    ft.land_tax_value_dollar.value,
    ft.total_tax_value_dollar.value,
    ft.lot_size_sqft.value,
    ft.calculated_total_living_area_sqft.value,
    ],
    County.ORANGE: [
        ft.finished_first_floor_sqft.value,
        ft.living_area_first_floor_sqft.value,
    ],
    County.LOS_ANGELES: [
        ft.building_condition.value,
    ],
}

class ZillowTransformer():

    _means = {}
    _medians = {}
    _modes = {}
    _features = []

    def __init__(self, county: County = None):
        self.county = county

    def fit(self, X: pd.DataFrame, y=None):
        for label, col in X.iteritems():
            try: 
                self._means[label] = col.mean()
                self._medians[label] = col.median()
                self._modes[label] = col.mode()
                self._features.append(label)
            except:
                pass

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        dataframe = X.copy(deep=True)

        dataframe[mft.nan_cnt.value] = dataframe.isna().sum(axis=1)

        # remove empty rows
        dataframe.dropna(axis=0, how='any', thresh=6, inplace=True)
        
        # new features
        dataframe = self._handle_transaction_date(dataframe)
        dataframe[mft.land_use_label.value] = dataframe[ft.land_use_type.value].replace(zd.property_land_use_type)
        dataframe[mft.county_name.value] = dataframe[ft.county_id.value].replace(zd.county_dict)
        # fix existing features
        dataframe[ft.latitude.value]  = dataframe[ft.latitude.value]  / 10e5
        dataframe[ft.longitude.value] = dataframe[ft.longitude.value] / 10e5

        dataframe = self._replace_nan_with_0(dataframe, _nan_to_zero['common'])
        dataframe = self._replace_nan_with_mean(dataframe, _nan_to_mean['common'])

        # replace categorical features with 0/1
        dataframe[ft.has_unpaid_tax.value].replace({'Y': 1., 'N': 0.}, inplace=True)
        dataframe[ft.has_fireplace.value].replace({True: 1., False: 0.}, inplace=True)
        dataframe[ft.has_spa.value].replace({True: 1., False: 0.}, inplace=True)

        dataframe[mft.has_pool.value] = dataframe[ft.pool_cnt.value]
        dataframe.loc[dataframe[ft.pool_cnt.value] > 0, mft.has_pool.value] = 1.

        dataframe[mft.has_fireplace.value] = 0.
        dataframe.loc[dataframe[ft.has_fireplace.value] == 1, mft.has_fireplace.value] = 1.
        dataframe.loc[dataframe[ft.fireplace_cnt.value] > 0, mft.has_fireplace.value] = 1.

        dataframe.drop(columns=_droplist['common'], inplace=True)

        if self.county == County.ORANGE:
            dataframe = self._replace_nan_with_0(dataframe, _nan_to_zero[County.ORANGE])
            dataframe = self._replace_nan_with_mean(dataframe, _nan_to_mean[County.ORANGE])
            dataframe.drop(columns=_droplist[County.ORANGE], inplace=True)

        elif self.county == County.VENTURA:
            dataframe = self._replace_nan_with_0(dataframe, _nan_to_zero[County.VENTURA])
            dataframe.drop(columns=_droplist[County.VENTURA], inplace=True)

        elif self.county == County.LOS_ANGELES:
            dataframe[ft.heating_system_type.value].fillna(13., inplace=True) # 13 is 'None'
            dataframe = self._replace_nan_with_mean(dataframe, _nan_to_mean[County.LOS_ANGELES])
            dataframe[mft.heating_label.value] = dataframe[ft.heating_system_type.value].replace(zd.heating_system_dict)
            dataframe.drop(columns=_droplist[County.LOS_ANGELES], inplace=True)

        else:
            dataframe.drop(columns=_droplist['remove_all'], inplace=True)

        dataframe.dropna(axis=1, thresh=100, inplace=True)

        return dataframe

    def _replace_nan_with_mean(self, df: pd.DataFrame, labels) -> pd.DataFrame:
        for label in labels:
            df[label + '_was_nan'] = df[label].isna()
            df[label + '_was_nan'].replace({True: 1., False: 0.}, inplace=True)
            df[label].fillna(math.floor( self._means[label] ), inplace=True)
        return df

    def _replace_nan_with_0(self, df: pd.DataFrame, labels) -> pd.DataFrame:
        # here we don't create a new column to indicate if the value was nan
        # because adding 0 instead of nan doesn't alter the column
        for label in labels:
            df[label].fillna(0., inplace=True)
        return df

    def _handle_transaction_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df[ft.transaction_date.value] = pd.to_datetime(df[ft.transaction_date.value], format='%Y-%m-%d')
        df[mft.transaction_month.value] = df[ft.transaction_date.value].dt.month_name()
        df[mft.transaction_month_day.value] = df[ft.transaction_date.value].dt.day
        df[mft.transaction_week_day.value] = df[ft.transaction_date.value].dt.day_name()
        df[mft.transaction_year.value] = df[ft.transaction_date.value].dt.year
        return df


class ZillowEncoder():

    _encoder: OneHotEncoder

    def __init__(self) -> None:
        self._encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

    def fit(self, df: pd.DataFrame) -> None:
        self._encoder.fit(df[_categorical_features['to transform']])

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        encoded = self._encoder.transform(df[_categorical_features['to transform']])
        df[ self._encoder.get_feature_names() ] = encoded
        df.drop(columns=_categorical_features['to drop'], axis=1, inplace=True)
        return df.astype(float)
