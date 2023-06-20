"""
This script computes the averaged ROI timeseries

@author: trianaa1
"""
import glob, os
import numpy as np

import nibabel as nib

from nilearn.masking import compute_epi_mask

###############################################################################
# Input variables: modify these accordingly

nii_path = '/m/cs/scratch/networks-pm/epeli/data/organized_videos/'
suffix = 'task-mergedvideoupsampled-denoised-24HMP-8Phys_HPF.nii' #T1w_desc-brain_mask.nii.gz
###############################################################################

#Make a list of files, subjects to preprocess
files = sorted(glob.glob(nii_path + f'/**/*{suffix}', recursive=True))

#Discard those subjects that will not be included
ban_list = ['sub-F36', 'sub-F102', 'sub-F103', 'sub-F108', 'sub-F119', 'sub-F129', 'sub-F137'] #avg FD > 0.5
files = [f for f in files if not any(ban in f for ban in ban_list)]

#Compute EPI masks
for file in files:
    head, tail = os.path.split(file)
    _, subject = os.path.split(head)
    mask_name = f'{head}/{subject}_mask.nii'
    if not os.path.exists(mask_name):
        mask = compute_epi_mask(file)
        nib.save(mask,mask_name)
    print(subject)