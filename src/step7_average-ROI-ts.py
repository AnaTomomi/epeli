"""
This script computes the averaged ROI timeseries

@author: trianaa1
"""
import glob, os
import numpy as np
import pandas as pd
from scipy.io import savemat, loadmat

import nibabel as nib
from nilearn.maskers import NiftiLabelsMasker

from sklearn.linear_model import LinearRegression

###############################################################################
# Input variables: modify these accordingly

#nii_path = '/m/cs/scratch/networks-pm/epeli/data/organized_videos/'
nii_path = '/m/nbe/scratch/fmri_epeli/brain_data/experiment/derivatives/denoise_new_smoothing'
ts_path = '/m/cs/scratch/networks-pm/epeli/data/timeseries'
atlas_name = 'haskins' #'brainnetome-child'
###############################################################################

#Make a list of files, subjects to preprocess
files = sorted(glob.glob(nii_path + f'/**/*24HMP-8Phys_HPF_smoothed10mm.nii', recursive=True))

#Discard those subjects that will not be included
ban_list = ['sub-F36', 'sub-F102', 'sub-F103', 'sub-F108', 'sub-F119', 'sub-F129', 'sub-F137'] #avg FD > 0.5
files = [f for f in files if not any(ban in f for ban in ban_list)]
#del files[13] #sub-F11 who has 3/4 videos for 6mm data

if atlas_name=='brainnetome-child':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_brainnetome-child.nii'
elif atlas_name=='haskins':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_haskins.nii'
elif atlas_name=='seitzman':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_seitzman.nii'
else:
    print('no atlas defined!')

#load the mask
masker = NiftiLabelsMasker(labels_img=atlas, standardize=True) #z-scored
           
#Compute the ROI-tsout
for file in files:
    head, tail = os.path.split(file)
    outfile = f'{ts_path}/{tail[:-4]}_{atlas_name}.csv'
    if os.path.exists(outfile):
        print(f'Node time series file for {file} already exists!')
    else:
        print(f'Creating node time series for {file} in {outfile}')
        time_series = masker.fit_transform(file)
        pd.DataFrame(time_series).to_csv(outfile, index=False, header=False)
sub=[]
for file in files:
    head, tail = os.path.split(file)
    _, tail = os.path.split(head)
    sub.append(tail)