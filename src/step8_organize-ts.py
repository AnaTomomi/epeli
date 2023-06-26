"""
This script organizes the time-series to be passed on to the ISCstats toolbox

@author: trianaa1
"""

import glob, os
import numpy as np
import pandas as pd
from scipy.io import savemat, loadmat

def organize_data(files):
    #input: list of file paths
    #output: numpy array
    
    #organize the controls
    sub = {}
    for file in files:
        head, tail = os.path.split(file)
        subject = tail.split("_")[0]
        sub[subject] = pd.read_csv(file, header=None)

    n_sub = len(sub)

    #organize the data, so that each slice in the z-axis is a matrix of TRsXsubjects
    data = np.zeros((n_tr, n_sub, n_rois))
    for roi in range(n_rois):
        for n_sub, key in enumerate(sub.keys()):
            data[:,n_sub,roi] = sub[key].loc[:,roi]
            print(key)
    return data

#Load the data
ts_path = '/m/cs/scratch/networks-pm/epeli/data/scrubbed_timeseries_10'
save_path = '/m/cs/scratch/networks-pm/epeli/data/isc_scrubbed_10'
atlas = 'haskins'
smoothing = '6mm'
files = sorted(glob.glob(ts_path + f'/**/*{smoothing}*{atlas}*.csv', recursive=True))
n_rois = 106
n_tr = 664

#Split the data in groups
controls = [file for file in files if 'sub-F' in file and len(file.split('sub-F')[1].split('_')[0]) == 2]
adhd = [file for file in files if 'sub-F' in file and len(file.split('sub-F')[1].split('_')[0]) == 3]

data = organize_data(controls)
data_dict = {"data": data, "label": "controls"}
savemat(f'{save_path}/tc_{smoothing}_{atlas}.mat', data_dict)        

data = organize_data(adhd)
data_dict = {"data": data, "label": "adhd"}
savemat(f'{save_path}/adhd_{smoothing}_{atlas}.mat', data_dict)   


#Print the subject list
sub_list = []
for file in files:
    head, tail = os.path.split(file)
    subject = tail.split("_")[0]
    sub_list.append(subject)

with open('/m/cs/scratch/networks-pm/epeli/data/isc_no-scrub/subject_list.txt', 'w') as f:
    for line in sub_list:
        f.write(f"{line}\n")