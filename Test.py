from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from Downloader import Downloader

username = 'kepeilei'
password = '297089702yuxiaO'
path = '/Users/DavidLei/PycharmProjects/untitled/testfile.geojson'
link: str = 'https://scihub.copernicus.eu/apihub/'

downloader = Downloader(username, password, link)
wkt = geojson_to_wkt(read_geojson(path))
downloader.search_polygon(wkt, '20151219', '20151229', str_platform_name='Sentinel-1', percentage=(0, 100))
downloader.download_products('/Users/DavidLei/PycharmProjects/untitled')
