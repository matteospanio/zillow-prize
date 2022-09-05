from os.path import dirname, join, realpath
import re

from typing import Tuple
import pandas as pd
from Zillow.transform import ZillowEncoder, ZillowTransformer

from Zillow.types import County, Features


county_dict = {
    County.VENTURA.value: 'Ventura',
    County.ORANGE.value: 'Orange',
    County.LOS_ANGELES.value: 'Los Angeles'
}

heating_system_dict = {
    1: 'Baseboard',
    2: 'Central',
    3: 'Coal',
    4: 'Convection',
    5: 'Electric',
    6: 'Forced air',
    7: 'Floor/Wall',
    8: 'Gas',
    9: 'Geo Thermal',
    10: 'Gravity',
    11: 'Heat Pump',
    12: 'Hot Water',
    13: 'None',
    14: 'Other',
    15: 'Oil',
    16: 'Partial',
    17: 'Propane',
    18: 'Radiant',
    19: 'Steam',
    20: 'Solar',
    21: 'Space/Suspended',
    22: 'Vent',
    23: 'Wood',
    24: 'Yes',
    25: 'Zoned',
}

air_conditioning_dict = {
    1: 'Central',
    2: 'Chilled Water',
    3: 'Evaporative Cooler',
    4: 'Geothermal',
    5: 'None',
    6: 'Other',
    7: 'Packaged AC',
    8: 'Partial',
    9: 'Refrigeration',
    10: 'Ventilation',
    11: 'Wall Unit',
    12: 'Window Unit',
    13: 'Yes',
}

property_land_use_type = {
    31 : 'Commercial/Office/Residential mix',
    46 : 'Multi-Story Store',
    47 : 'Store/Office mix',
    246: 'Duplex (2 Units)',
    247: 'Triplex (3 Units)',
    248: 'Quadruplex (4 Units)',
    260: 'Residential General',
    261: 'Single Family Residential',
    262: 'Rural Residence',
    263: 'Mobile Home',
    264: 'Townhouse',
    265: 'Cluster Home',
    266: 'Condominium',
    267: 'Cooperative',
    268: 'Row House',
    269: 'Planned Unit Development',
    270: 'Residential Common Area',
    271: 'Timeshare',
    273: 'Bungalow',
    274: 'Zero Lot Line',
    275: 'Manufactured, Modular, Prefabricated Homes',
    276: 'Patio Home',
    279: 'Inferred Single Family Residential',
    290: 'Vacant Land - General',
    291: 'Residential Vacant Land',
}


def _find_dataset(file: str) -> str:
    '''find dataset in Zillow package'''
    return join(dirname(realpath(__file__)), f"dataset/{file}")


def get_raw_features(year: int) -> pd.DataFrame:
    '''load features per year'''
    if year == 2016:
        return pd.read_csv(_find_dataset("properties_2016.csv"), low_memory=False)
    elif year == 2017:
        return pd.read_csv(_find_dataset("properties_2017.csv"), low_memory=False)
    else:
        raise Exception('You can get only data from 2016 or 2017')


def get_raw_y(year: int) -> pd.DataFrame:
    '''load y per year'''
    if year == 2016:
        return pd.read_csv(_find_dataset("train_2016_v2.csv"))
    elif year == 2017:
        return pd.read_csv(_find_dataset("train_2017.csv"))
    else:
        raise Exception('You can get only data from 2016 or 2017')


def merge_x_y(x: pd.DataFrame, y: pd.DataFrame, on=None, with_duplicates: bool = False, left_index: bool = False, right_index: bool = False) -> pd.DataFrame:
    if with_duplicates == False:
        y = y.sort_values(Features.transaction_date.value).drop_duplicates(Features.parcel_id.value, keep = "last")
    return pd.merge(y, x, on = on, how = "inner", left_index=left_index, right_index=right_index)


def read_unique(name: str, data_series: pd.DataFrame):
    print(f"{name} has {len(data_series)} transactions on {len(data_series.parcelid.unique())} different properties.")


def split_x_y(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    x = dataset.drop(Features.log_error.value, axis=1)
    y = dataset[Features.log_error.value]

    return x, y

def get_dataset(year: int = None, county: County = None) -> pd.DataFrame:
    '''load merged data per county and year'''
    data_2016 = pd.read_csv(_find_dataset("2016_data_exploration.csv"))
    data_2017 = pd.read_csv(_find_dataset("2017_data_exploration.csv"))

    ventura_2016 = data_2016[data_2016[Features.county_id.value] == county_dict[County.VENTURA.value]]
    ventura_2017 = data_2017[data_2017[Features.county_id.value] == county_dict[County.VENTURA.value]]

    orange_2016 = data_2016[data_2016[Features.county_id.value] == county_dict[County.ORANGE.value]]
    orange_2017 = data_2017[data_2017[Features.county_id.value] == county_dict[County.ORANGE.value]]

    los_angeles_2016 = data_2016[data_2016[Features.county_id.value] == county_dict[County.LOS_ANGELES.value]]
    los_angeles_2017 = data_2017[data_2017[Features.county_id.value] == county_dict[County.LOS_ANGELES.value]]

    if year == 2016:
        if county == County.VENTURA:
            return ventura_2016
        elif county == County.ORANGE:
            return orange_2016
        elif county == County.LOS_ANGELES:
            return los_angeles_2016
        elif county == None:
            return data_2016
        else:
            raise Exception('There is no such county')
    elif year == 2017:
        if county == County.VENTURA:
            return ventura_2017
        elif county == County.ORANGE:
            return orange_2017
        elif county == County.LOS_ANGELES:
            return los_angeles_2017
        elif county == None:
            return data_2017
        else:
            raise Exception('There is no such county')
    elif year == None:
        if county == County.VENTURA:
            return merge_years(ventura_2016, ventura_2017)
        elif county == County.ORANGE:
            return merge_years(orange_2016, orange_2017)
        elif county == County.LOS_ANGELES:
            return merge_years(los_angeles_2016, los_angeles_2017)
        elif county == None:
            return merge_years(data_2016, data_2017)
        else:
            raise Exception('There is no such county')
    else:
        raise Exception('You can get only data from 2016 or 2017')


def merge_years(dataset_1: pd.DataFrame, dataset_2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([dataset_1, dataset_2], axis=0, ignore_index=True)


def get_train_dataset(county: County = None) -> pd.DataFrame:
    data = pd.read_csv(_find_dataset("train_dataset.csv"))
    if county == County.VENTURA:
        return data[data[Features.county_id.value] == County.VENTURA.value]
    elif county == County.ORANGE:
        return data[data[Features.county_id.value] == County.ORANGE.value]
    elif county == County.LOS_ANGELES:
        return data[data[Features.county_id.value] == County.LOS_ANGELES.value]
    elif county == None:
        return data
    else:
        raise Exception('There is no such county')

def get_validation_dataset(county: County = None) -> pd.DataFrame:
    data = pd.read_csv(_find_dataset("validation_dataset.csv"))
    if county == County.VENTURA:
        return data[data[Features.county_id.value] == County.VENTURA.value]
    elif county == County.ORANGE:
        return data[data[Features.county_id.value] == County.ORANGE.value]
    elif county == County.LOS_ANGELES:
        return data[data[Features.county_id.value] == County.LOS_ANGELES.value]
    elif county == None:
        return data
    else:
        raise Exception('There is no such county')

def get_train_and_validation_dataset(county: County = None) -> pd.DataFrame:
    data = pd.read_csv(_find_dataset("train_total_dataset.csv"))
    if county == County.VENTURA:
        return data[data[Features.county_id.value] == County.VENTURA.value]
    elif county == County.ORANGE:
        return data[data[Features.county_id.value] == County.ORANGE.value]
    elif county == County.LOS_ANGELES:
        return data[data[Features.county_id.value] == County.LOS_ANGELES.value]
    elif county == None:
        return data
    else:
        raise Exception('There is no such county')

def get_test_dataset(county: County = None) -> pd.DataFrame:
    data = pd.read_csv(_find_dataset("test_dataset.csv"))
    if county == County.VENTURA:
        return data[data[Features.county_id.value] == County.VENTURA.value]
    elif county == County.ORANGE:
        return data[data[Features.county_id.value] == County.ORANGE.value]
    elif county == County.LOS_ANGELES:
        return data[data[Features.county_id.value] == County.LOS_ANGELES.value]
    elif county == None:
        return data
    else:
        raise Exception('There is no such county')

def get_preprocessed_data(county: County = None):

    train = get_train_dataset(county)
    validation = get_validation_dataset(county)
    test = get_test_dataset(county)

    preprocessor = ZillowTransformer(county)
    preprocessor.fit(train)

    train = preprocessor.transform(train)
    validation = preprocessor.transform(validation)
    test = preprocessor.transform(test)

    encoder = ZillowEncoder()
    encoder.fit(train)

    train = encoder.transform(train)
    validation = encoder.transform(validation)
    test = encoder.transform(test)

    return train, validation, test

