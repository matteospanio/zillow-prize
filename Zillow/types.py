from enum import Enum


class County(Enum):
    VENTURA = 1286
    ORANGE = 2061
    LOS_ANGELES = 3101


class Features(Enum):
    parcel_id = 'parcelid'
    log_error = 'logerror'
    transaction_date = 'transactiondate'
    air_conditioning_type = 'airconditioningtypeid'
    architectural_style = 'architecturalstyletypeid'
    basement_sqft = 'basementsqft'
    bathroom_cnt = 'bathroomcnt'
    bedroom_cnt = 'bedroomcnt'
    building_class = 'buildingclasstypeid'
    building_condition = 'buildingqualitytypeid'
    calculated_bath_nbr = 'calculatedbathnbr'
    deck_type = 'decktypeid'
    finished_first_floor_sqft = 'finishedfloor1squarefeet'
    calculated_total_living_area_sqft = 'calculatedfinishedsquarefeet'
    finished_living_area_sqft = 'finishedsquarefeet12'
    perimeter_living_area_sqft = 'finishedsquarefeet13'
    total_area_sqft = 'finishedsquarefeet15'
    living_area_first_floor_sqft = 'finishedsquarefeet50'
    finished_and_unfinished_sqft = 'finishedsquarefeet6'
    fips = 'fips'
    fireplace_cnt ='fireplacecnt'
    full_bath_cnt = 'fullbathcnt'
    garage_car_cnt = 'garagecarcnt'
    garage_sqft = 'garagetotalsqft'
    has_spa = 'hashottuborspa'
    heating_system_type = 'heatingorsystemtypeid'
    latitude = 'latitude'
    longitude = 'longitude'
    lot_size_sqft = 'lotsizesquarefeet'
    pool_cnt = 'poolcnt'
    pool_size = 'poolsizesum'
    pool_is_spa = 'pooltypeid10'
    pool_has_spa = 'pooltypeid2'
    not_spa_pool = 'pooltypeid7'
    county_land_use_code = 'propertycountylandusecode'
    land_use_type = 'propertylandusetypeid'
    allowed_land_use_description = 'propertyzoningdesc'
    raw_census_tract_and_block = 'rawcensustractandblock'
    city_id = 'regionidcity'
    county_id = 'regionidcounty'
    neighborhood_id = 'regionidneighborhood'
    zip_id = 'regionidzip'
    room_cnt = 'roomcnt'
    floors_type = 'storytypeid'
    three_quarter_bath_cnt = 'threequarterbathnbr'
    construction_material = 'typeconstructiontypeid'
    structures_built_cnt = 'unitcnt'
    patio_in_yard_sqft = 'yardbuildingsqft17'
    storage_building_in_yard_sqft = 'yardbuildingsqft26'
    year_built = 'yearbuilt'
    floors_cnt = 'numberofstories'
    has_fireplace = 'fireplaceflag'
    structure_tax_value_dollar = 'structuretaxvaluedollarcnt'
    total_tax_value_dollar = 'taxvaluedollarcnt'
    assessment_year= 'assessmentyear'
    land_tax_value_dollar = 'landtaxvaluedollarcnt'
    tax_assessed= 'taxamount'
    has_unpaid_tax= 'taxdelinquencyflag'
    unpaid_tax_year = 'taxdelinquencyyear'
    census_tract_and_block= 'censustractandblock'


class MoreFeatures(Enum):
    county_name = 'county_name'
    nan_cnt = 'nan_cnt'
    land_use_label = 'land_use_label'
    air_cooler_label = 'air_cooler_label'
    transaction_month = 'transaction_month'
    transaction_month_day = 'transaction_month_day'
    transaction_week_day = 'transaction_week_day'
    transaction_year = 'transaction_year'
    has_pool = 'has_pool'
    has_fireplace = 'has_fireplace'
    heating_label = 'heating_label'
