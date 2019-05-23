import rasterio
import numpy as np
from PIL import Image as img
import png

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL2A_20190502T001619_N0211_R059_T60WWD_20190502T022958.SAFE/' \
       'GRANULE/L2A_T60WWD_A011239_20190502T001617/IMG_DATA/R10m/T60WWD_20190502T001619'

blue = rasterio.open(path+'_B02_10m.jp2')
green = rasterio.open(path+'_B03_10m.jp2')
red = rasterio.open(path+'_B04_10m.jp2')
blue = blue.read(1)
green = green.read(1)
red = red.read(1)
length = len(red)
data = np.zeros([length, length, 3], dtype=np.uint16)

for i in range(length):
    for j in range(length):
        data[i, j, 0] = red[i, j]
        data[i, j, 1] = green[i, j]
        data[i, j, 2] = blue[i, j]

with open('test.png', 'wb') as file:
    writer = png.Writer(width=data.shape[1], height=data.shape[0], bitdepth=16)
    datalist = data.reshape(-1, data.shape[1] * data.shape[2]).tolist()
    writer.write(file, datalist)

