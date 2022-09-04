import pandas as pd
import Zillow.data as zd
from Zillow.types import County, Features as ft, MoreFeatures as mft

categorical_features = {
    ft.air_conditioning_type.value,
    ft.architectural_style.value,
    ft.building_class.value,
    ft.building_condition.value,
    ft.deck_type.value,
    ft.floors_type.value,
    ft.heating_system_type.value,
    ft.pool_has_spa.value,
    ft.pool_is_spa.value,
    ft.has_spa.value,
    ft.has_fireplace.value,
    ft.land_use_type.value,
    ft.zip_id.value,
    ft.county_id.value,
    ft.neighborhood_id.value,
    ft.not_spa_pool.value,
}

_droplist = {
    'common': [
        'Unnamed: 0',
        ft.parcel_id.value,
        ft.transaction_date.value,
        ft.air_conditioning_type.value,
        ft.land_use_type.value,
        ft.county_id.value,
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
    ],
    County.ORANGE: [
        ft.building_condition.value,
        ft.finished_and_unfinished_sqft.value,
        ft.heating_system_type.value,
    ],
    County.VENTURA: [
        ft.building_condition.value,
        ft.finished_first_floor_sqft.value,
        ft.total_area_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.pool_size.value,
        ft.patio_in_square_yard.value,
        ft.storage_building_square_yard.value,
    ],
    County.LOS_ANGELES: [
        ft.finished_first_floor_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.finished_and_unfinished_sqft.value,
        ft.garage_car_cnt.value,
        ft.garage_sqft.value,
        ft.pool_size.value,
        ft.room_cnt.value,
        ft.patio_in_square_yard.value,
        ft.storage_building_square_yard.value,
    ],
    'remove_all': [
        'Unnamed: 0',
        ft.room_cnt.value,
        ft.garage_sqft.value,
        ft.garage_car_cnt.value,
        ft.storage_building_square_yard.value,
        ft.pool_size.value,
        ft.patio_in_square_yard.value,
        ft.living_area_first_floor_sqft.value,
        ft.total_area_sqft.value,
        ft.finished_first_floor_sqft.value,
        ft.heating_system_type.value,
        ft.finished_and_unfinished_sqft.value,
        ft.building_condition.value,
        ft.parcel_id.value,
        ft.transaction_date.value,
        ft.air_conditioning_type.value,
        ft.land_use_type.value,
        ft.county_id.value,
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
    ]
}

def process_data(df):
    # create new numerical features
    df[mft.nan_cnt.value] = df.isna().sum(axis=1)

    # transform transaction date
    df[ft.transaction_date.value] = pd.to_datetime(df[ft.transaction_date.value],
                                               format='%Y-%m-%d')
    df[mft.transaction_month.value] = df.transactiondate.dt.month_name()
    df[mft.transaction_month_day.value] = df.transactiondate.dt.day
    df[mft.transaction_week_day.value] = df.transactiondate.dt.day_name()

    # create new categorical features
    df[mft.land_use_label.value] = df[ft.land_use_type.value].replace(zd.property_land_use_type)
    df[mft.air_cooler_label.value] = df[ft.air_conditioning_type.value].replace(zd.air_conditioning_dict)
    df[mft.county_name.value] = df[ft.county_id.value].replace(zd.county_dict)

    # fix existing features
    df[ft.latitude.value]  = df[ft.latitude.value]  / 10e5
    df[ft.longitude.value] = df[ft.longitude.value] / 10e5

    df[ft.has_unpaid_tax.value] = df[ft.has_unpaid_tax.value].fillna(0)
    df[ft.has_unpaid_tax.value] = df[ft.has_unpaid_tax.value].replace({'Y': 1})
    df[ft.unpaid_tax_year.value] = df[ft.unpaid_tax_year.value].fillna(0.)

    df[ft.has_fireplace.value] = df[ft.has_fireplace.value].fillna(0.)
    df[ft.has_fireplace.value] = df[ft.has_fireplace.value].replace({True: 1.})
    df[ft.fireplace_cnt.value] = df[ft.fireplace_cnt.value].fillna(0.)

    df[ft.has_spa.value] = df[ft.has_spa.value].fillna(0)
    df[ft.has_spa.value] = df[ft.has_spa.value].replace({True: 1})

    df[ft.pool_cnt.value] = df[ft.pool_cnt.value].fillna(0)

    df[ft.structures_built_cnt.value] = df[ft.structures_built_cnt.value].fillna(0)

    df['has_fireplace'] = 0
    df.loc[df[ft.has_fireplace.value] == 1, 'has_fireplace'] = 1
    df.loc[df[ft.fireplace_cnt.value] > 0, 'has_fireplace'] = 1

    # drop columns
    df = df.drop(columns=_droplist['remove_all'], axis=1)
    df = df.dropna(axis=1, thresh=100)

    return df
