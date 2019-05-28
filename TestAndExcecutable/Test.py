from sentinelsat import read_geojson, geojson_to_wkt
from Downloader import Downloader
import StringProcessor as process
import geopandas

username = 'kepeilei'
password = '297089702yuxiaO'
path = '/Users/DavidLei/PycharmProjects/untitled/testfile.geojson'
link: str = 'https://scihub.copernicus.eu/apihub/'
from_satelite: str = 'Sentinel-2'
package_info = list()

downloader = Downloader(username, password, link)
wkt = geojson_to_wkt(read_geojson(path))
downloader.search_polygon(wkt, '20190501', '20190503', str_platform_name=from_satelite, percentage=(0, 100))
for key, value in downloader.products.items():
    if "S2B_MSIL2A" in str(value):
        # print('downloading')
        # print(key)
        # print(value)
        package_info.append(str(value))
        # print(package_info)
        downloader.download_one(str(key), path='/Users/DavidLei/PycharmProjects/untitled')

for original_string in package_info:
    process.divide_string(original_string)
# df_products = downloader.download_products('/Users/DavidLei/PycharmProjects/untitled', False)
gdf_products: geopandas.geodataframe = downloader.download_geoproduct(path='/Users/DavidLei/PycharmProjects/untitled'
                                                                      , download_file=False)
print(gdf_products.count())
print(downloader.download_json())
gdf_products.head()
gdf_products.plot()
