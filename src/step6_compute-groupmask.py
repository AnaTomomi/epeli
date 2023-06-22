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

nii_path = '/m/cs/scratch/networks-pm/epeli/data/organized_videos/'
ts_path = '/m/cs/scratch/networks-pm/epeli/data/group_masks'
atlas_name = 'seitzman-set1' #'haskins' #'brainnetome-child'
vol_size = [91,109,91]
###############################################################################

#Make a list of files, subjects to preprocess
files = sorted(glob.glob(nii_path + f'/**/*24HMP-8Phys_HPF_smoothed6mm.nii', recursive=True))

#Discard those subjects that will not be included
ban_list = ['sub-F36', 'sub-F102', 'sub-F103', 'sub-F108', 'sub-F119', 'sub-F129', 'sub-F137'] #avg FD > 0.5
files = [f for f in files if not any(ban in f for ban in ban_list)]

#Compute the group mask
group_mask_mult_name = f'{ts_path}/group_mask_mult.nii'
group_mask_sum_name = f'{ts_path}/group_mask_sum95.nii'
if not os.path.exists(group_mask_mult_name) or not os.path.exists(group_mask_sum_name):
    group_mask_mult = np.ones(vol_size)
    group_mask_sum = np.zeros(vol_size)
    for file in files:
        head, tail = os.path.split(file)
        _, subject = os.path.split(head)
        mask = nib.load(f'{nii_path}{subject}/{subject}_mask.nii')
        data = mask.get_fdata()
        group_mask_mult = group_mask_mult*data
        group_mask_sum = group_mask_sum+data
    thr = np.amax(group_mask_sum)*0.95
    group_mask_sum[group_mask_sum<thr] = 0 #set values that are not in the 95% percentile of the mask to zero
    # i.e. if a voxel is in 95% of the cases, it stays
    group_mask_sum[group_mask_sum>0] = 1

    group_mask_nii = nib.Nifti1Image(group_mask_mult, mask.affine, mask.header)
    nib.save(group_mask_nii,group_mask_mult_name)
    group_mask_nii = nib.Nifti1Image(group_mask_sum, mask.affine, mask.header)
    nib.save(group_mask_nii,group_mask_sum_name)
    print(f'Group mask computed for {len(files)} files')
    
#Multiply the group mask by the atlas
if atlas_name=='brainnetome-child':
    atlas = '/m/cs/scratch/networks-pm/atlas/Brainnetome/BrainnetomeChild/CHILD_ATLAS_224.nii.gz'
elif atlas_name=='haskins':
    atlas = '/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/Haskins2mm.nii'
elif atlas_name=='seitzman-set1':
    atlas = '/m/cs/scratch/networks-pm/atlas/300_ROI_Set/seitzman_set1.nii'
else:
    print('no atlas defined!')
    
gmask = nib.load(group_mask_mult_name)
gmask_data = gmask.get_fdata()
atlas_nii = nib.load(atlas)
atlas_data = atlas_nii.get_fdata()
atlas_data = np.reshape(atlas_data, vol_size)

atlas_mask = gmask_data*atlas_data
atlas_mask_nii = nib.Nifti1Image(atlas_mask, atlas_nii.affine, atlas_nii.header)
masked_atlas = f'{ts_path}/group_mask_{atlas_name}.nii'
nib.save(atlas_mask_nii,masked_atlas)
print(f'Masked {atlas_name} atlas with group mask')

