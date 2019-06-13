import rasterio
import numpy as np
from PIL import Image as img
from osgeo import gdal, ogr, osr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL1C_20190502T234629_N0207_R073_T01WCP_20190503T012751.SAFE' \
       '/GRANULE/L1C_T01WCP_A011253_20190502T234630/IMG_DATA/T01WCP_20190502T234629'

fourteen_bit = 16384
eight_bit = 255
image_pixel = 10980


def get_colorTuple(rgb):
    mesh_rgb = rgb[:, :-1, :]
    colorTuple = mesh_rgb.reshape((mesh_rgb.shape[0] * mesh_rgb.shape[1]), 3)
    colorTuple = np.insert(colorTuple, 3, 1.0, axis=1)
    return colorTuple


def linear_scale(original):
    print('to linear scaling')
    counter = 0
    new = (255.0 / original.max() * (original - original.min())).astype(np.uint8)
    for i in range(len(new)):
        counter += 1
        if counter % 100 == 0:
            print(f'dealing with {counter}th row')
        for j in range(len(new[0])):
            if new[i, j, 0] == 0 and new[i, j, 1] == 0 and new[i, j, 2] == 0:
                new[i, j] = [255, 255, 255, 0]
            else:
                new[i, j, 3] = 255
    return new


def non_liner_scale(original, threshold_low, threshold_high):
    print('non-linear scaling')
    counter = 0
    slope = 255 / (fourteen_bit - threshold_high - threshold_low)
    offset = - threshold_low * slope
    new = np.copy(original)
    # print(new[0, 0])
    for i in range(len(new)):
        counter += 1
        if counter % 100 == 0:
            # print(new[i, 0])
            print(f'dealing with {counter}th row')
        for j in range(len(new[0])):
            new[i, j, 0] = max(0, min(255, (new[i, j, 0] * slope - offset)))
            new[i, j, 1] = max(0, min(255, (new[i, j, 1] * slope - offset)))
            new[i, j, 2] = max(0, min(255, (new[i, j, 2] * slope - offset)))
    return new.astype(np.uint8)


def to_rgb(file_path, is_linear, ignore_low=1250, ignore_high=2750):
    blue = rasterio.open(file_path + '_B02.jp2')
    green = rasterio.open(file_path + '_B03.jp2')
    red = rasterio.open(file_path + '_B04.jp2')
    print('reading blue')
    blue = blue.read(1)
    print('reading green')
    green = green.read(1)
    print('reading red')
    red = red.read(1)
    length = len(red)
    data = np.zeros([length, length, 4], dtype=np.uint16)
    data[:, :, 3] = 2 ** 16
    print(f'red has max {np.amax(red)} and min {np.amin(red)}')
    print(f'blue has max {np.amax(blue)} and min {np.amin(blue)}')
    print(f'green has max {np.amax(green)} and min {np.amin(green)}')

    print('to np array')
    data[:, :, 0] = red
    data[:, :, 1] = green
    data[:, :, 2] = blue
    # for i in range(length):
    #     print(f'writing {i}th row')
    #     for j in range(length):
    #         data[i, j, 0] = red[i, j]
    #         data[i, j, 1] = green[i, j]
    #         data[i, j, 2] = blue[i, j]

    if is_linear:
        rescaled = linear_scale(data)
    else:
        rescaled = non_liner_scale(data, ignore_low, ignore_high)
    return rescaled


def export_photo(data, name='my.png'):
    photo = img.fromarray(data)
    photo.save(name)
    photo.show()


def non_linear_transparent(new):
    # print(new[0, 0])
    print("non-linear transparency")
    red_min = np.amin(new[:, :, 0])
    green_min = np.amin(new[:, :, 1])
    blue_min = np.amin(new[:, :, 2])
    counter = 0
    for i in range(len(new)):
        counter += 1
        if counter % 100 == 0:
            print(f'dealing with {counter}th row')
        for j in range(len(new[0])):
            if new[i, j, 0] <= red_min and new[i, j, 1] <= green_min and new[i, j, 2] <= blue_min:
                new[i, j] = [255, 255, 255, 0]
            else:
                new[i, j, 3] = 255
    return new


def GetExtent(gt, cols, rows):
    ext = []
    xarr = [0, cols]
    yarr = [0, rows]

    for px in xarr:
        for py in yarr:
            x = gt[0] + (px * gt[1]) + (py * gt[2])
            y = gt[3] + (px * gt[4]) + (py * gt[5])
            ext.append([x, y])
        yarr.reverse()
    return ext


def ReprojectCoords(coords, src_srs, tgt_srs):
    trans_coords = []
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x, y in coords:
        x, y, z = transform.TransformPoint(x, y)
        trans_coords.append([x, y])
    return trans_coords


def get_corner_cood(file_path):
    ds = gdal.Open(file_path + '_B02.jp2')
    gt = ds.GetGeoTransform()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    ext = GetExtent(gt, cols, rows)
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(ds.GetProjection())
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(ds.GetProjection())
    tgt_srs = src_srs.CloneGeogCS()
    return ReprojectCoords(ext, src_srs, tgt_srs)


def get_colorTuple(rgb):
    mesh_rgb = rgb[:, :-1, :]
    colorTuple = mesh_rgb.reshape((mesh_rgb.shape[0] * mesh_rgb.shape[1]), 4)
    return colorTuple


def get_full_cood(file_path=path):
    coods = get_corner_cood(file_path)
    for cood in coods:
        if cood[0] < 0:
            cood[0] = cood[0] + 360
    cood_array = np.zeros([image_pixel, image_pixel], dtype=(float, 2))
    cood_array[0][0] = coods[0]
    cood_array[image_pixel - 1][0] = coods[1]
    cood_array[image_pixel - 1][image_pixel - 1] = coods[2]
    cood_array[0][image_pixel - 1] = coods[3]
    left_step = ((coods[1][0]-coods[0][0]) / (image_pixel - 1), (coods[1][1]-coods[0][1]) / (image_pixel - 1))
    right_step = ((coods[2][0]-coods[3][0]) / (image_pixel - 1), (coods[2][1]-coods[3][1]) / (image_pixel - 1))
    for i in range(image_pixel):
        cood_array[i][0] = (cood_array[0][0][0] + i * left_step[0], cood_array[0][0][1] + i * left_step[1])
        cood_array[i][image_pixel - 1] = (cood_array[0][image_pixel - 1][0] + i * right_step[0],
                                          cood_array[0][image_pixel - 1][1] + i * right_step[1])

    for row in range(image_pixel):
        origin = cood_array[row][0]
        step = (cood_array[row][10979] - origin) / (image_pixel - 1)
        for col in range(image_pixel):
            cood_array[row][col] = (origin[0] + col * step[0], origin[1] + col * step[1])
    return cood_array


def transform_north(lons, lats, north_crs, north_xform_crs):
    pts = north_crs.transform_points(north_xform_crs, lons, lats)
    x = pts[..., 0]
    y = pts[..., 1]
    return x, y


def test_method():
    stuff = to_rgb(path, is_linear=False)
    stuff = non_linear_transparent(stuff)

    north_crs = ccrs.Orthographic(65, 90)
    north_globe = ccrs.Globe(semiminor_axis=90)
    north_xform_crs = ccrs.Geodetic(globe=north_globe)

    lons = np.zeros(image_pixel * image_pixel)
    lats = np.zeros(image_pixel * image_pixel)
    coodinates = get_full_cood(path)
    coodList = np.ndarray.flatten(coodinates)
    color_list = get_colorTuple(stuff)
    for i in range(image_pixel * image_pixel):
        lons[i] = coodList[2 * i]
        lats[i] = coodList[2 * i + 1]

    fig = plt.figure()
    lons, lats = transform_north(lons, lats, north_crs, north_xform_crs)
    GeoAxes._pcolormesh_patched = Axes.pcolormesh
    ax = plt.axes(projection=north_crs)
    ax.pcolormesh(lons, lats, color_list, transform=north_crs, color=color_list)
    plt.savefig('output.png', format="png", bbox_inches='tight', dpi=1200)
    # export_photo(stuff, 'WCP.png')


test_method()
