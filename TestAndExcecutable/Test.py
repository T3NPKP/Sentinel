from sentinelsat import read_geojson, geojson_to_wkt
from Downloader import Downloader
import geopandas

username = 'kepeilei'
password = '297089702yuxiaO'
path = '/Users/DavidLei/PycharmProjects/untitled/testfile.geojson'
link: str = 'https://scihub.copernicus.eu/apihub/'
from_satelite: str = 'Sentinel-2'

downloader = Downloader(username, password, link)
wkt = geojson_to_wkt(read_geojson(path))
downloader.search_polygon(wkt, '20190501', '20190503', str_platform_name=from_satelite, percentage=(0, 100))
for key, value in downloader.products.items():
    if "S2B_MSIL1C" in str(value):
        print('downloading')
        print(key)
        print(value)
        downloader.download_one(str(key), path='/Users/DavidLei/PycharmProjects/untitled')

# df_products = downloader.download_products('/Users/DavidLei/PycharmProjects/untitled', False)
gdf_products: geopandas.geodataframe = downloader.download_geoproduct(path='/Users/DavidLei/PycharmProjects/untitled'
                                                                      , download_file=False)
print(gdf_products.count())
print(downloader.download_json())
gdf_products.head()
gdf_products.plot()
