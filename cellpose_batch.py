# Script to process multiple image z stacks within one folder at once
import os
import glob
from cellpose import models, io
############################################## USER INPUTS FIELD #######################################################
# REPLACE WITH YOUR IMAGE FOLDER PATHS
# Your images are saved as home_dir/xxx/xxx.png
img_seq_dir = r'X:\Kou\20220620_tutorial\flow_avg'
# DEFINE CELLPOSE MODEL
modeltype = 'cyto2'
# DEFINE OTHER PARAMETERS
diameter = 15.0
flow_threshold = 0.2
########################################################################################################################

dir_lst = os.listdir(img_seq_dir)

for dir in dir_lst:
    print('-----------------------------------------------------------------------------------------------------------')
    print('Start processing: ', dir)
    files = glob.glob(os.path.join(img_seq_dir, dir, '*.tif'))
    model = models.CellposeModel(gpu=True, model_type=modeltype)
    chan = [[0, 0]]
    for filename in files:
        print('Processing: ', filename)
        img = io.imread(filename)
        masks, flows, styles = model.eval(img, diameter=diameter, flow_threshold=flow_threshold, channels=chan)

        # save results so you can load in gui
        io.masks_flows_to_seg(img, masks, flows, None, filename, chan)
