#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:32:22 2023

@author: trianaa1

This script visualize the FD for the 4 videos in the EPELI project
"""

import os, glob
import numpy as np
import pandas as pd

import nibabel as nib
from nilearn.maskers import NiftiLabelsMasker

###############################################################################
path = "/m/cs/scratch/networks-pm/epeli/results/fd_reorganized"
optimal_thr = 0.5

#nii_path = '/m/cs/scratch/networks-pm/epeli/data/organized_videos/'
nii_path = '/m/nbe/scratch/fmri_epeli/brain_data/experiment/derivatives/denoise_new_smoothing'
ts_path = '/m/cs/scratch/networks-pm/epeli/data/scrubbed_timeseries_10'
atlas_name = 'brainnetome-child' #'brainnetome-child'
###############################################################################


# list of banned subjects based on Roosa's info
meta = pd.read_excel("/m/cs/scratch/networks-pm/epeli/data/subjects_list.xlsx")
meta = meta[meta["include"]==1]
include = meta["Unnamed: 0"].to_list()
subjects_info = meta[["Unnamed: 0", "group"]]
subjects_info.set_index("Unnamed: 0", inplace=True)

# load FD and get the volumes that need to be scrubbed
df = pd.read_excel(f'{path}/fd_all.xlsx', index_col=0)
df = df.where((df > optimal_thr).mean(axis=1) <= 0.10) #adjust the percent accordingly
scrub = df[df.isna().any(axis=1)].index.tolist()

# Prepare the NII data
files = sorted(glob.glob(nii_path + f'/**/*24HMP-8Phys_HPF_smoothed6mm.nii', recursive=True))
ban_list = ['sub-F36', 'sub-F102', 'sub-F103', 'sub-F108', 'sub-F119', 'sub-F129', 'sub-F137'] #avg FD > 0.5
files = [f for f in files if not any(ban in f for ban in ban_list)]
#del files[13]

if atlas_name=='brainnetome-child':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_brainnetome-child.nii'
elif atlas_name=='haskins':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_haskins.nii'
elif atlas_name=='seitzman':
    atlas = '/m/cs/scratch/networks-pm/epeli/data/group_masks/group_mask_seitzman.nii'
else:
    print('no atlas defined!')
    
masker = NiftiLabelsMasker(labels_img=atlas, standardize=True) #z-scored

# Start scrubbing and compute the ROI-ts
for file in files:
    head, tail = os.path.split(file)
    outfile = f'{ts_path}/{tail[:-4]}_{atlas_name}.csv'
    if os.path.exists(outfile):
        print(f'Node time series file for {outfile} already exists!')
    else:
        print(f'Creating node time series for {file} in {outfile}')
        nii = nib.load(file)
        nii_data = nii.get_fdata()
        nii_data = np.delete(nii_data, scrub, axis=3)
        
        new_nii = nib.Nifti1Image(nii_data, nii.affine, nii.header)
                
        time_series = masker.fit_transform(new_nii)
        pd.DataFrame(time_series).to_csv(outfile, index=False, header=False)