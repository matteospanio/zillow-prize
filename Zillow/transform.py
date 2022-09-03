from Zillow.types import County, Features as ft


general_droplist = [
    #'airconditioningtypeid', #no orange
    'architecturalstyletypeid',
    'basementsqft',
    'buildingclasstypeid',
    'decktypeid',
    #'buildingqualitytypeid', #solo los angeles
    'calculatedbathnbr',
    'finishedfloor1squarefeet',
    'finishedsquarefeet6',
    'finishedsquarefeet12',
    'finishedsquarefeet13',
    'finishedsquarefeet15',
    'finishedsquarefeet50',
    #'fireplacecnt',        #no los angeles
    'fullbathcnt',
    #'garagecarcnt',        #no los angeles
    #'garagetotalsqft',     #no los angeles
    #'hashottuborspa',      #no orange
    'poolsizesum',
    #'pooltypeid10',        #no orange
    #'pooltypeid2',         #solo ventura
    'storytypeid',
    'threequarterbathnbr',
    'typeconstructiontypeid',
    'yardbuildingsqft17',
    'yardbuildingsqft26',
]


droplist = {
    'common': [
        ft.architectural_style.value,
        ft.basement_sqft.value,
        ft.building_class.value,
        ft.deck_type.value,
        ft.perimeter_living_area_sqft.value,
        ft.pool_size.value,
        ft.floors_type.value,
        ft.storage_building_square_yard.value,
        ft.three_quarter_bath_cnt.value,
        ft.assessment_year.value,
    ],
    County.ORANGE: [
        ft.air_conditioning_type.value,
        ft.building_condition.value,
        ft.finished_and_unfinished_sqft.value,
        ft.has_spa.value,
        ft.heating_system_type.value,
        ft.pool_is_spa.value,
        ft.pool_has_spa.value,
        ft.allowed_land_use_description.value,
        ft.construction_material.value,
        ft.has_fireplace.value,
    ],
    County.VENTURA: [
        ft.bathroom_cnt.value,
        ft.building_condition.value,
        ft.finished_first_floor_sqft.value,  
        ft.total_area_sqft.value,
    ],
    County.LOS_ANGELES: [
        ft.finished_first_floor_sqft.value,
        ft.total_area_sqft.value,
        ft.living_area_first_floor_sqft.value,
        ft.finished_and_unfinished_sqft.value,
        ft.fireplace_cnt.value,
        ft.pool_has_spa.value,
        ft.construction_material.value,
        ft.patio_in_square_yard.value,
        ft.floors_cnt.value
    ],
}

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

def process_data(df):
    df = df.dropna(axis=1, thresh=100)
    return df
