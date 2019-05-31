import rasterio
import numpy as np
from PIL import Image as img

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL1C_20190502T234629_N0207_R073_T01WCR_20190503T012751.SAFE' \
       '/GRANULE/L1C_T01WCR_A011253_20190502T234630/IMG_DATA/T01WCR_20190502T234629'

fourteen_bit = 16384
eight_bit = 255


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


def test_method():
    stuff = to_rgb(path, is_linear=False)
    stuff = non_linear_transparent(stuff)
    export_photo(stuff, 'my-nonlinear.png')


test_method()


