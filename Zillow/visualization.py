from mpl_toolkits.basemap import Basemap

map_code_property_land_use_type = {
    31 : 1,
    46 : 2,
    47 : 3,
    246: 4,
    247: 5,
    248: 6,
    260: 7,
    261: 8,
    262: 9,
    263: 10,
    264: 11,
    265: 12,
    266: 13,
    267: 14,
    268: 15,
    269: 16,
    270: 17,
    271: 18,
    273: 19,
    274: 20,
    275: 21,
    276: 22,
    279: 23,
    290: 24,
    291: 25,
}


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
