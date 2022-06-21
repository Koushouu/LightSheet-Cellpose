# Script to extract the X Y coordinates of the blobs identified. Output csv file of all the coordinates
import numpy as np
import glob
import os
import multiprocessing
import time
############################################## USER INPUTS FIELD #######################################################
# REPLACE WITH YOUR SEGMENTATION FOLDER PATHS
# Your segmentation results are saved as home_dir/xxx/z_*_seg.npy
img_seq_dir = r'X:\Kou\20220620_tutorial\flow_avg'
coord_csv_dir = r'X:\Kou\20220620_tutorial\coord_csv'
# Define the number of CPUs
n_cpu = 20
########################################################################################################################


def coordinates_extract(z, filepath):
    print('start processing ' + filepath + ' z = ' + str(z))
    npy = np.load(filepath, allow_pickle=True).item()
    masks = npy['masks']
    maxid = np.amax(masks)
    # Initialize the list to store the x and y coordinates
    xlist = []
    ylist = []
    for i in range(1, maxid + 1):
        coord = np.where(masks == i)
        x, y = int(np.mean(coord[0])), int(np.mean(coord[1]))
        xlist.append(x)
        ylist.append(y)

    zlist = [z for _ in range(1, maxid + 1)]
    return [xlist, ylist, zlist]


if __name__ == "__main__":
    # Get the list of z stack
    folder_lst = os.listdir(img_seq_dir)
    for folder in folder_lst:
        print("---------------------Start processing " + folder + "-----------------------------")
        file_lst = glob.glob(os.path.join(img_seq_dir, folder, 'z_*_seg.npy'))
        xlist_all = []
        ylist_all = []
        zlist_all = []
        # Start timer to analyse the performance
        start_time = time.perf_counter()
        with multiprocessing.Pool(n_cpu) as pool:
            results = pool.starmap(coordinates_extract, enumerate(file_lst))
        for coord in results:
            xlist_all += coord[0]
            ylist_all += coord[1]
            zlist_all += coord[2]
        np.save(os.path.join(coord_csv_dir, folder), [xlist_all, ylist_all, zlist_all])
        # Creating csv...
        coord = np.transpose([xlist_all, ylist_all, zlist_all])
        coordname = os.path.join(coord_csv_dir, folder) + '.csv'
        np.savetxt(coordname, coord, delimiter=",")
        finish_time = time.perf_counter()
        print(f"Program finished in {finish_time - start_time} seconds")