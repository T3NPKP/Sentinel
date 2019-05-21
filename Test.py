from sentinelsat import read_geojson, geojson_to_wkt
from Downloader import Downloader

username = 'kepeilei'
password = '297089702yuxiaO'
path = '/Users/DavidLei/PycharmProjects/untitled/testfile.geojson'
link: str = 'https://scihub.copernicus.eu/apihub/'

downloader = Downloader(username, password, link)
wkt = geojson_to_wkt(read_geojson(path))
downloader.search_polygon(wkt, '20190501', '20190503', str_platform_name='Sentinel-1', percentage=(0, 100))
df_products = downloader.download_products('/Users/DavidLei/PycharmProjects/untitled')
gdf_products = downloader.download_geoproduct('/Users/DavidLei/PycharmProjects/untitled')