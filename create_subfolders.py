import os

###################################### User Input Field ###############################################################
project_dir = r'X:\Kou\20220621_tutorial'
#######################################################################################################################

dirs = ['raw_tif', 'img_seq', 'flow_avg', 'coord_csv', 'coord_tif']

for dir in dirs:
    fullpath = os.path.join(project_dir, dir)
    os.mkdir(fullpath)