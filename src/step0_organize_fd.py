#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:32:22 2023

@author: merzonl1

The script cut and merge video data for Roosa.
It save 4 videos separately + one merged file
"""

import os
import pandas as pd
import numpy as np
import math

path_bids = '/m/nbe/scratch/fmri_epeli/brain_data/experiment/bids'
path_fmriprep ="/m/nbe/scratch/fmri_epeli/brain_data/experiment/derivatives/fmriprep"
savepath = "/m/cs/scratch/networks-pm/epeli/results/fd_reorganized"

tr = 0.594

suf = "task-video_desc-confounds_timeseries.tsv"

sub_list = next(os.walk(path_fmriprep))[1]
ban_list = ['logs', 'sourcedata']
sub_list = [x for x in sub_list if x not in ban_list]
sub_list.sort()

############### videos ###################

task = "video"

# duration of the videos in seconds
video_1_dur_s = 139.83
video_2_dur_s = 119.04
video_3_dur_s = 119.04
video_4_dur_s = 139.88

# duration of the videos in TRs
video_1_dur_n = math.floor(video_1_dur_s/tr)
video_2_dur_n = math.floor(video_2_dur_s/tr)
video_3_dur_n = math.floor(video_3_dur_s/tr)
video_4_dur_n = math.floor(video_4_dur_s/tr)


for sub in sub_list:
    
    print(sub)
        
    #read denoised nifti file and timing data from bids
    file_fd = f'{path_fmriprep}/{sub}/func/{sub}_{suf}'
    file_timing = f'{path_bids}/{sub}/func/{sub}_task-video_events.tsv'
    
    if os.path.isfile(file_fd) and os.path.isfile(file_timing):
        fd = pd.read_csv(file_fd, sep ='\t')
        fd = fd["framewise_displacement"]
        timing = pd.read_csv(file_timing, sep ='\t')
    
        video_dur = {'video_1':video_1_dur_n, 'video_2':video_2_dur_n, 'video_3':video_3_dur_n, 'video_4':video_4_dur_n}

        #presentation crashed, so we have only 3 videos for this subject        
        if sub == "sub-F11":
            video_dur = {'video_1':video_1_dur_n, 'video_2':video_2_dur_n, 'video_3':video_3_dur_n}


        total_dur_n = fd.shape[-1]
        all_idx = list(range(total_dur_n))
        indexes_for_all_videos = []
    
        #collect start and end indexes for all videos   
        all_cuts = []
        for v in dict(sorted(video_dur.items())):    
            #define which volumes we need
            start_t = timing.loc[timing.trial_type ==v, "onset"]
            start_idx = math.ceil(start_t/tr)
            end_idx =  start_idx + video_dur[v]
        
            indexes_for_all_videos = indexes_for_all_videos + all_idx[start_idx:end_idx]
    
            #cut out one video
            cut_fd = fd.loc[start_idx:end_idx]
            all_cuts.append(cut_fd)
    
        # merge all cut fd in the right order and save
        new_fd = pd.concat(all_cuts)
    
        new_fd.to_csv(f'{savepath}/{sub}_task-{task}_fd-reorganized.csv')
    
        print(sub, "done")

print("video viewing done")


