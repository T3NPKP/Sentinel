from osgeo import gdal
import sys
from fileinfo import file_info

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL2A_20190502T001619_N0211_R059_T60WWD_20190502T022958.SAFE' \
       '/GRANULE/L2A_T60WWD_A011239_20190502T001617/IMG_DATA/R10m/T60WWD_20190502T001619'

blue_info = file_info()
blue_info.init_from_name((path + '_B02_10m.jp2'))
blue_data = gdal.Open((path + '_B02_10m.jp2'), gdal.GA_ReadOnly)
blue_band = blue_data.GetRasterBand(1)

green_info = file_info()
green_info.init_from_name((path + '_B03_10m.jp2'))
green_data = gdal.Open((path + '_B03_10m.jp2'), gdal.GA_ReadOnly)
green_band = green_data.GetRasterBand(1)

red_info = file_info()
red_info .init_from_name((path + '_B04_10m.jp2'))
red_data = gdal.Open((path + '_B04_10m.jp2'), gdal.GA_ReadOnly)
red_band = red_data.GetRasterBand(1)

print("Band Type={}".format(gdal.GetDataTypeName(blue_band.DataType)))
print("Amount of band={}".format(blue_data.RasterCount))

out_format = 'GTiff'
out_file_name = 'out.tif'

Driver = gdal.GetDriverByName(out_format)
if Driver is None:
    print('Format driver %s not found, pick a supported driver.' % out_format)
    sys.exit(1)

DriverMD = Driver.GetMetadata()
if 'DCAP_CREATE' not in DriverMD:
    print(
        'Format driver %s does not support creation and piecewise writing.\nPlease select a format that does, '
        'such as GTiff (the default) or HFA (Erdas Imagine).' % out_format)
    sys.exit(1)

xsize_original = blue_data.RasterXSize
ysize_original = blue_data.RasterYSize
geotransform_original = blue_data.GetGeoTransform()
ulx = geotransform_original[0]
uly = geotransform_original[3]
lrx = ulx + geotransform_original[1] * xsize_original
lry = uly + geotransform_original[5] * ysize_original
band_type = blue_band.DataType
psize_x = geotransform_original[1]
psize_y = geotransform_original[5]

geotransform = [ulx, psize_x, 0, uly, 0, psize_y]
xsize = int((lrx - ulx) / geotransform[1] + 0.5)
ysize = int((lry - uly) / geotransform[5] + 0.5)
num_bands = 3

out_file = Driver.Create(out_file_name, xsize, ysize, num_bands,
                         band_type)
if out_file is None:
    print('Creation failed, terminating gdal_merge.')
    sys.exit(1)

out_file.SetGeoTransform(geotransform)
out_file.SetProjection(blue_data.GetProjection())

blue_info.copy_into(out_file, 1, 1, None)
green_info.copy_into(out_file, 1, 2, None)
red_info.copy_into(out_file, 1, 3, None)

min_raster = blue_band.GetMinimum()
max_raster = blue_band.GetMaximum()
if not min_raster or not max_raster:
    (min_raster, max_raster) = blue_band.ComputeRasterMinMax(True)
print("Min={:.3f}, Max={:.3f}".format(min_raster, max_raster))

if blue_band.GetOverviewCount() > 0:
    print("blue_band has {} overviews".format(blue_band.GetOverviewCount()))

if blue_band.GetRasterColorTable():
    print("blue_band has a color table with {} entries".format(blue_band.GetRasterColorTable().GetCount()))
