#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:32:22 2023

@author: merzonl1

The script cut and merge video data for Roosa.
It save 4 videos separately + one merged file
"""

import nibabel
import os
import pandas as pd
import numpy as np
import math

path_denoised = '/m/nbe/scratch/fmri_epeli/brain_data/experiment/derivatives/denoise_new'
path_bids = '/m/nbe/scratch/fmri_epeli/brain_data/experiment/bids'
path_fmriprep ="/m/nbe/scratch/fmri_epeli/brain_data/experiment/derivatives/fmriprep"

tr = 0.594

suf = "denoised-24HMP-8Phys_HPF"

sub_list = next(os.walk(path_denoised))[1]
ban_list = ['denoise_new', '__pycache__',  '.bidsignore', "scripts_for_denoising"]
#ban_list =['sub-F136', 'sub-F27']
sub_list = [x for x in sub_list if x not in ban_list]
sub_list.sort()
sub_list =['sub-F28', 'sub-F104', 'sub-F117', 'sub-F118', 'sub-F121', 'sub-F122', 'sub-F123', 'sub-F124']


############### videos ###################

task = "video"

video_1_dur_s = 139.83
video_2_dur_s = 119.04
video_3_dur_s = 119.04
video_4_dur_s = 139.88

video_1_dur_n = math.floor(video_1_dur_s/tr)
video_2_dur_n = math.floor(video_2_dur_s/tr)
video_3_dur_n = math.floor(video_3_dur_s/tr)
video_4_dur_n = math.floor(video_4_dur_s/tr)

#sub = 'sub-F01'
#{}
#print("processing", task)

for sub in sub_list:
    
    print(sub)
        
    #read denoised nifti file and timing data from bids
    file_fmri = f'{path_denoised}/{sub}/{sub}_task-{task}_{suf}.nii'
    file_timing = f'{path_bids}/{sub}/func/{sub}_task-video_events.tsv'
    
    #check if there is a denoised file already
    if not os.path.exists(file_fmri):
        print(sub, "skipped, not ready")
        continue  

    #check if the participant has already been processed
    if os.path.exists(f'{path_denoised}_smoothing/{sub}/'):
        print(sub, "skipped")
        continue
    
    if not os.path.exists(f'{path_denoised}_smoothing/{sub}/'):    
        os.mkdir(f'{path_denoised}_smoothing/{sub}')
    
    img = nibabel.load(file_fmri)
    timing = pd.read_csv(file_timing, sep ='\t')
    
    video_dur = {'video_1':video_1_dur_n, 'video_2':video_2_dur_n, 'video_3':video_3_dur_n, 'video_4':video_4_dur_n}

    #presentation crashed, so we have only 3 videos for this subject        
    if sub == "sub-F11":
        video_dur = {'video_1':video_1_dur_n, 'video_2':video_2_dur_n, 'video_3':video_3_dur_n}


    data = np.asarray(img.dataobj)
    total_dur_n = data.shape[-1]
    all_idx = list(range(total_dur_n))
    indexes_for_all_videos = []
    
    #collect start and end indexes for all videos    
    for v in dict(sorted(video_dur.items())):
        
        #define which volumes we need
        start_t = timing.loc[timing.trial_type ==v, "onset"]
        start_idx = math.ceil(start_t/tr)

        end_idx =  start_idx + video_dur[v]
        
        indexes_for_all_videos = indexes_for_all_videos + all_idx[start_idx:end_idx]
    
        #cut out one video
        cut_img = img.slicer[:,:,:,start_idx:end_idx]
        
        # save new nifti file
        path_save = f'{path_denoised}_smoothing/{sub}/{sub}_task-{v}-{suf}.nii'
        nibabel.save(cut_img, path_save)
        
    data = data[..., indexes_for_all_videos]
    cut_img = img.__class__(data, affine=img.affine, header=img.header, extra=img.extra)
    
    path_save = f'{path_denoised}_smoothing/{sub}/{sub}_task-mergedvideo-{suf}.nii'
    nibabel.save(cut_img, path_save)
    
    print(sub, "done")

print("video viewing done")


