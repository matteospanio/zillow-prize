from typing import Tuple
from mpl_toolkits.basemap import Basemap
import pandas as pd

from Zillow.data import property_land_use_type
from Zillow.types import MoreFeatures as mft

def create_labels_for_non_zero_land_use_types(df: pd.DataFrame) -> Tuple[dict, dict]:
    labels = {}
    color_map = {}
    for i, (key, label) in enumerate(property_land_use_type.items()):
        if len(df[df[mft.land_use_label.value] == label]) > 0:
            labels[key] = label
            color_map[label] = i
    return labels, color_map


class ZillowMap(Basemap):

    def __init__(self, ax):
        super().__init__(projection='lcc', resolution='f',
            lat_0=34, lon_0=-118.3,
            width=230000, height=250000, ax=ax)
        self.draw_map_basics()

    def draw_map_basics(self):
        self.drawmapboundary(fill_color='#d8eaf3')
        self.fillcontinents(color='#f6fbd7',lake_color='#d8eaf3')
        self.drawcoastlines(color='gray')
        self.drawcounties(color='darkgrey', linewidth=.3)
