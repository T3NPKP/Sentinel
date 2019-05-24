import rasterio
import numpy as np
from PIL import Image as img

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL2A_20190502T001619_N0211_R059_T60WWD_20190502T022958.SAFE/' \
       'GRANULE/L2A_T60WWD_A011239_20190502T001617/IMG_DATA/R10m/T60WWD_20190502T001619'

fourteen_bit = 16384
eight_bit = 255


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


def to_rgb(file_path):
    blue = rasterio.open(path + '_B02_10m.jp2')
    green = rasterio.open(path + '_B03_10m.jp2')
    red = rasterio.open(path + '_B04_10m.jp2')
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

    # rescaled = linear_scale(data)
    rescaled = non_liner_scale(data, 2000, 2000)

    photo = img.fromarray(rescaled, 'RGB')
    photo.save('my1.png')
    photo.show()
