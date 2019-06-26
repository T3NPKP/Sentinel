from sentinelsat import read_geojson, geojson_to_wkt
from Downloader import Downloader
import StringProcessor as process
import zipfile
import os

username = 'kepeilei'
password = '297089702yuxiaO'
path = '/Users/DavidLei/PycharmProjects/untitled/testfile.geojson'
link: str = 'https://scihub.copernicus.eu/apihub/'
from_satelite: str = 'Sentinel-2'
package_info = list()
keys = []

downloader = Downloader(username, password, link)
wkt = geojson_to_wkt(read_geojson(path))
downloader.search_polygon(wkt, '20190501', '20190503', str_platform_name=from_satelite, percentage=(0, 100))
f = open('FileList.txt', 'w+')
for key, value in downloader.products.items():
    if "S2B_MSIL1C" in str(value):
        # print('downloading')
        # print(key)
        # print(value)
        package_info.append(str(value))
        keys.append(str(key))
        print(value['title'])
        downloader.download_one(str(key), path='/Users/DavidLei/PycharmProjects/untitled')
        zf = zipfile.ZipFile(value['title'] + '.zip')
        zf.extractall()
        zf.close()
        f.write(value['filename'] + '\n')
        os.remove('/Users/DavidLei/PycharmProjects/untitled/' + value['title'] + '.zip')

# num = 3
# print(f'downloading {package_info[num]}')
# downloader.download_one(keys[num], path='/Users/DavidLei/PycharmProjects/untitled')
# print(keys)

processed_strings = []
for original_string in package_info:
    processed_strings.append(process.divide_string(original_string))

# print(processed_strings)
# df_products = downloader.download_products('/Users/DavidLei/PycharmProjects/untitled', False)
# gdf_products: geopandas.geodataframe = downloader.download_geoproduct(path='/Users/DavidLei/PycharmProjects/untitled'
#                                                                      , download_file=True)
# print(gdf_products.count())
# print(downloader.download_json())
# gdf_products.head()
# gdf_products.plot()
