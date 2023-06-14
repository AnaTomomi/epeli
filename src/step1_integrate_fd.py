#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:32:22 2023

@author: trianaa1

This script visualize the FD for the 4 videos in the EPELI project
"""

import os
import numpy as np
import pandas as pd

path = "/m/cs/scratch/networks-pm/epeli/results/fd_reorganized"
savepath = "/m/cs/scratch/networks-pm/epeli/results/fd_reorganized"

# list of banned subjects based on Roosa's info
meta = pd.read_excel("/m/cs/scratch/networks-pm/epeli/data/subjects_list.xlsx")
meta = meta[meta["include"]==1]
include = meta["Unnamed: 0"].to_list()
subjects_info = meta[["Unnamed: 0", "group"]]
subjects_info.set_index("Unnamed: 0", inplace=True)

# get the files
suf = "task-video_fd-reorganized.csv"
files = [f for f in os.listdir(path) if f.endswith(suf)]
files = [f for f in files if any(sub in f for sub in include)]
files.sort()

# set the video duration
video1_dur = 235
video2_dur = 200
video3_dur = 200
video4_dur = 235

# divide the data in the video sequences
video1, video2, video3, video4 = {}, {}, {}, {}


for file in files: 
    sub = file[0:8]
    data = pd.read_csv(os.path.join(path, file))["framewise_displacement"]
    video1[sub] = data[0:video1_dur+1]
    video2[sub] = data[video1_dur+1:video1_dur+video2_dur+2]
    video3[sub] = data[video1_dur+video2_dur+2:video1_dur+video2_dur+video3_dur+3]
    video4[sub] = data[video1_dur+video2_dur+video3_dur+3:]

video1 = pd.DataFrame.from_dict(video1)
video2 = pd.DataFrame.from_dict(video2)
video3 = pd.DataFrame.from_dict(video3)
video4 = pd.DataFrame.from_dict(video4)

df = pd.concat([video1, video2, video3, video4])

df.to_excel(f'{savepath}/fd_all.xlsx')