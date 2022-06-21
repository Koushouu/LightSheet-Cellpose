# Script to extract and average the image flow

import multiprocessing
import time
import os
from skimage.io import imsave
import numpy as np

############################################## USER INPUTS FIELD #######################################################
project_dir = r"X:\Kou\20220620_tutorial"
########################################################################################################################


img_seq_dir = os.path.join(project_dir, 'img_seq')
flow_avg_dir = os.path.join(project_dir, 'flow_avg')


def flow_extract(filename, img_size, folder):
    npy_filepath = os.path.join(img_seq_dir, folder, filename)
    flowavg_filepath = os.path.join(flow_avg_dir, folder, filename[:-4] + '_flowavg.tif')
    print('start processing' + npy_filepath)
    npy = np.load(npy_filepath, allow_pickle=True).item()
    flows = npy['flows']
    RGB2D = flows[0][0]
    RGBmean = np.zeros([img_size[0], img_size[1]])
    for x in range(img_size[0]):
        for y in range(img_size[1]):
            RGBmean[x, y] = np.mean(RGB2D[x][y])
    imsave(flowavg_filepath, RGBmean)


if __name__ == "__main__":
    # Get a list of z stack
    folder_lst = os.listdir(img_seq_dir)
    # loop through the z stacks
    for folder in folder_lst:
        # Create the corresponding folder in the flow_avg folder
        os.mkdir(os.path.join(flow_avg_dir, folder))
        # Get the list of npy (segmentation) files
        file_lst = os.listdir(os.path.join(img_seq_dir, folder))
        file_lst_npy = []
        for file in file_lst:
            if file.endswith(".npy"):
                file_lst_npy.append(file)
        # Get the image size
        npy = np.load(os.path.join(img_seq_dir, folder, file_lst_npy[0]), allow_pickle=True).item()
        flowsize = np.shape(npy['flows'][0][0])
        img_size = [flowsize[0], flowsize[1]]
        # Define the number of CPUs ####################################################################################
        n_cpu = 40
        pool = multiprocessing.Pool(n_cpu)
        # Start timer to analyse the performance
        start_time = time.perf_counter()
        # Start parallel processing
        processes = [pool.apply_async(flow_extract, args=(filename, img_size, folder, )) for filename in file_lst_npy]
        result = [p.get() for p in processes]
        finish_time = time.perf_counter()
        print(f"Program finished in {finish_time - start_time} seconds")
