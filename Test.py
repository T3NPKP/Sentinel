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
downloader.search_polygon(wkt, '20190502', '20190503', str_platform_name=from_satelite, percentage=(0, 100))
#df_products = downloader.download_products('/Users/DavidLei/PycharmProjects/untitled', False)
gdf_products = downloader.download_geoproduct('/Users/DavidLei/PycharmProjects/untitled', False)
print(gdf_products.count())
gdf_products.head()
gdf_products.plot()
