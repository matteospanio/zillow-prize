from os.path import dirname, join, realpath
from typing import Tuple
import pandas as pd


categorical_features: list[str] = [
    'airconditioningtypeid',
    'architecturalstyletypeid',
    ''
]


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
        y = y.sort_values("transactiondate").drop_duplicates("parcelid",keep = "last")
    return pd.merge(y, x, on = "parcelid", how = "inner")


def read_unique(name: str, data_series: pd.DataFrame):
    print(f"{name} has total {len(data_series)} records and {len(data_series.parcelid.unique())} are unique.")


def split_x_y(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    x = dataset.drop('logerror', axis=1)
    y = dataset.logerror

    return x, y
