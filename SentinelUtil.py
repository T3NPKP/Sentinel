import cv2
from matplotlib import image as mpimg
import numpy as np

path = '/Users/DavidLei/PycharmProjects/untitled/S2B_MSIL2A_20190502T001619_N0211_R059_T60WWD_20190502T022958.SAFE/' \
       'GRANULE/L2A_T60WWD_A011239_20190502T001617/IMG_DATA/R10m/T60WWD_20190502T001619'

img_blue = mpimg.imread(path + '_B02_10m.jp2')
img_green = mpimg.imread(path + '_B03_10m.jp2')
img_red = mpimg.imread(path + '_B04_10m.jp2')

multichannel_img = np.zeros((img_blue.shape[0], img_blue.shape[1], 3))

multichannel_img[:, :, 0] = img_blue
multichannel_img[:, :, 1] = img_green
multichannel_img[:, :, 2] = img_red

cv2.imwrite('product.png', multichannel_img)
