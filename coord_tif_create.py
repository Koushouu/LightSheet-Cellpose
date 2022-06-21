# Create 3D tif from the csv created
import os
from skimage.io import imread, imsave
import numpy as np
from numpy import genfromtxt

##################################### User input field #################################################################
home_dir = r'X:\Kou\20220620_tutorial'

########################################################################################################################
coord_csv_dir = os.path.join(home_dir, 'coord_csv')
coord_tif_dir = os.path.join(home_dir, 'coord_tif')
raw_tif_dir = os.path.join(home_dir, 'raw_tif')

file_lst = os.listdir(coord_csv_dir)
folder_lst = []
for file in file_lst:
    if file.endswith(".csv"):
        folder_lst.append(file[:-4])

for folder in folder_lst:
    # Read in the raw tif and create a zero matrix of the same size
    raw_tif = imread(os.path.join(raw_tif_dir, folder))
    coord_vol = np.zeros_like(raw_tif)
    # Read the csv
    coord_csv = genfromtxt(os.path.join(coord_csv_dir, folder + '.csv'), delimiter=',').astype(int)
    # Create an output name
    coord_tif_path = os.path.join(coord_tif_dir, folder)

    for coord in coord_csv:
        [x, y, z] = coord
        # Write the coordinate pattern to coord_vol
        coord_vol[z, x - 1:x + 3, y:y + 2] = 1
        coord_vol[z, x:x + 2, y - 1:y + 3] = 1

    imsave(coord_tif_path, coord_vol)


