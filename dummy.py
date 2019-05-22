from satpy.scene import Scene
from satpy import find_files_and_readers
from datetime import datetime

files = find_files_and_readers(base_dir="/Users/DavidLei/PycharmProjects/untitled")

scn = Scene(filenames=files)
scn.load(['true_color'])
scn.save_dataset('true_color', filename='true_color_S2_gnc_tutorial' + '.png')