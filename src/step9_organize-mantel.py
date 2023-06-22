"""
This script organizes the time-series to be passed on to the ISCstats toolbox

@author: trianaa1
"""

import glob, os
import numpy as np
import pandas as pd
import re
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
ts_path = '/m/cs/scratch/networks-pm/epeli/data/timeseries'
save_path = '/m/cs/scratch/networks-pm/epeli/data/isc'
atlas = 'seitzman'
files = sorted(glob.glob(ts_path + f'/**/*{atlas}*.csv', recursive=True))
n_rois = 300
n_tr = 870

#exclude subjects
banned_list = ['sub-F106']
files = [f for f in files if not any(ban in f for ban in banned_list)]

#Organize the timeseries
data = organize_data(files)
data_dict = {"data": data, "label": "all"}
savemat(f'{save_path}/all_{atlas}.mat', data_dict)        

#Organize the behavioral data according to the subject list
beh_data = pd.read_csv('/m/cs/scratch/networks-pm/epeli/data/EPELI_aggregate_data.csv')
beh_data = beh_data[["Participant", "MR_Ohjaimen.keskikulmanopeus"]]

participants_order = [re.search('sub-(F[0-9]+)', f).group(1) for f in files]

# Set Participant as index and reindex
beh_data.set_index('Participant', inplace=True)
beh_data = beh_data.reindex(participants_order)
beh_data.to_excel(f'{save_path}/behavioral_{atlas}.xlsx')

#Print the subject list
sub_list = []
for file in files:
    head, tail = os.path.split(file)
    subject = tail.split("_")[0]
    sub_list.append(subject)

with open(f'{save_path}/subject_list.txt', 'w') as f:
    for line in sub_list:
        f.write(f"{line}\n")