from os.path import dirname, join, realpath

from typing import Tuple
import pandas as pd

from Zillow.types import County, Features


county_dict = {
    County.VENTURA.value: 'Ventura',
    County.ORANGE.value: 'Orange',
    County.LOS_ANGELES.value: 'Los Angeles'
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


def find_path(file: str) -> str:
    return join(dirname(realpath(__file__)), f"dataset/{file}")


def get_features(year: int) -> pd.DataFrame:
    if year == 2016:
        return pd.read_csv(find_path("properties_2016.csv"), low_memory=False)
    elif year == 2017:
        return pd.read_csv(find_path("properties_2017.csv"), low_memory=False)
    else:
        raise Exception('You can get only data from 2016 or 2017')


def get_y(year: int) -> pd.DataFrame:
    if year == 2016:
        return pd.read_csv(find_path("train_2016_v2.csv"))
    elif year == 2017:
        return pd.read_csv(find_path("train_2017.csv"))
    else:
        raise Exception('You can get only data from 2016 or 2017')


def merge_x_y(x: pd.DataFrame, y: pd.DataFrame, with_duplicates: bool = False) -> pd.DataFrame:
    if with_duplicates == False:
        y = y.sort_values(Features.transaction_date.value).drop_duplicates(Features.parcel_id.value, keep = "last")
    return pd.merge(y, x, on = Features.parcel_id.value, how = "inner")


def read_unique(name: str, data_series: pd.DataFrame):
    print(f"{name} has total {len(data_series)} records and {len(data_series.parcelid.unique())} are unique.")


def split_x_y(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    x = dataset.drop(Features.log_error.value, axis=1)
    y = dataset[Features.log_error.value]

    return x, y


def load_dataset(year: int) -> pd.DataFrame:
    '''load merged data'''
    if year == 2016:
        return pd.read_csv(find_path("2016_data_exploration.csv"))
    elif year == 2017:
        return pd.read_csv(find_path("2017_data_exploration.csv"))
    else:
        raise Exception('You can get only data from 2016 or 2017')
