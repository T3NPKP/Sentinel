import rasterio
import numpy as np
from PIL import Image as img

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL2A_20190502T001619_N0211_R059_T60WWD_20190502T022958.SAFE/' \
       'GRANULE/L2A_T60WWD_A011239_20190502T001617/IMG_DATA/R10m/T60WWD_20190502T001619'

fourteen_bit = 16384
eight_bit = 255


def get_colorTuple(rgb):
    mesh_rgb = rgb[:,:-1,:]
    colorTuple = mesh_rgb.reshape((mesh_rgb.shape[0] * mesh_rgb.shape[1]), 3)
    colorTuple = np.insert(colorTuple, 3, 1.0, axis=1)
    # for t in colorTuple:
    #     if t [0] < 0.0001 and t[1] < 0.0001 and t[2] < 0.0001:
    #         t[0] = 1
    #         t[1] = 1
    #         t[2] = 1
    #         t[3] = 0
    return colorTuple


def linear_scale(original):
    new = (255.0 / original.max() * (original - original.min())).astype(np.uint8)
    return new


def non_liner_scale(original, threshold_low, threshold_high):
    slope = 255 / (fourteen_bit - threshold_high - threshold_low)
    offset = - threshold_low * slope
    new = np.copy(original)
    for i in range(len(new)):
        print(f'non-linear dealing with {i}th row')
        for j in range(len(new[0])):
            new[i, j, 0] = max(0, min(255, (new[i, j, 0] * slope - offset)))
            new[i, j, 1] = max(0, min(255, (new[i, j, 1] * slope - offset)))
            new[i, j, 2] = max(0, min(255, (new[i, j, 2] * slope - offset)))
    return new.astype(np.uint8)


def to_rgb(file_path, is_linear, ignore_low = 2000, ignore_high = 2000):
    blue = rasterio.open(file_path + '_B02_10m.jp2')
    green = rasterio.open(file_path + '_B03_10m.jp2')
    red = rasterio.open(file_path + '_B04_10m.jp2')
    blue = blue.read(1)
    green = green.read(1)
    red = red.read(1)
    length = len(red)
    data = np.zeros([length, length, 3], dtype=np.uint16)
    print(f'red has max {np.amax(red)} and min {np.amin(red)}')
    print(f'blue has max {np.amax(blue)} and min {np.amin(blue)}')
    print(f'green has max {np.amax(green)} and min {np.amin(green)}')

    print('to np array')
    for i in range(length):
        print(f'writing {i}th row')
        for j in range(length):
            data[i, j, 0] = red[i, j]
            data[i, j, 1] = green[i, j]
            data[i, j, 2] = blue[i, j]

    if is_linear:
        rescaled = linear_scale(data)
    else:
        rescaled = non_liner_scale(data, ignore_low, ignore_high)
    return rescaled


def export_photo(data):
    photo = img.fromarray(data, 'RGB')
    photo.save('my1.png')
    photo.show()

