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
import seaborn as sns
import matplotlib.pyplot as plt

def optimize_threshold(df, subjects_info, min_timepoints=505, min_controls=20, min_patients=20, percentage=0.1):
    # Create a copy of the dataframe
    df_copy = df.copy()
    
    # Initialize the optimal threshold and subjects
    optimal_thr = None
    optimal_subjects = None
    
    # Get the minimum and maximum rating values in the dataframe
    min_val, max_val = 0.5, 1

    # Iterate over a range of thresholds
    for thr in np.linspace(min_val, max_val, 16):  # 100 is the number of steps, it can be adjusted
        # Discard rows where any subject's rating is above the threshold
        #df_copy = df.where(df <= thr).dropna() #This is a harsh scrub
        df_copy = df.where((df > thr).mean(axis=1) <= percentage).dropna() #this scrub is per percentage
        
        # Get the remaining subjects
        remaining_subjects = df_copy.columns
        
        # Check the conditions
        # Number of timepoints is minimum 606
        # Number of patients and controls are minimum 20
        if (len(df_copy) >= min_timepoints and
            (subjects_info.loc[remaining_subjects, 'group'] == 1.0).sum() >= min_controls and
            (subjects_info.loc[remaining_subjects, 'group'] == 2.0).sum() >= min_patients):
            
            # If conditions are met, update the optimal threshold and subjects
            optimal_thr = thr
            optimal_subjects = remaining_subjects
            break

    # If no optimal solution was found, print an error message
    if optimal_thr is None:
        print("No optimal solution was found.")
        return None

    # Return the optimal threshold and subjects
    return optimal_thr, optimal_subjects.tolist()

path = "/m/cs/scratch/networks-pm/epeli/results/fd_reorganized"

# list of banned subjects based on Roosa's info
meta = pd.read_excel("/m/cs/scratch/networks-pm/epeli/data/subjects_list.xlsx")
meta = meta[meta["include"]==1]
include = meta["Unnamed: 0"].to_list()
subjects_info = meta[["Unnamed: 0", "group"]]
subjects_info.set_index("Unnamed: 0", inplace=True)

# load FD 
df = pd.read_excel(f'{path}/fd_all.xlsx', index_col=0)

########################### Start optimization ################################

# define the list of subjects sorted by the number of "bad" volumes (i.e. FD>0.5)
# the list goes from the subject with most "bad" volumes to the least. 
threshold = 0.5
count_larger_than_threshold = df.apply(lambda x: (x > threshold).sum())
sorted_counts = count_larger_than_threshold.sort_values(ascending=False)
sorted_subjects = sorted_counts.index.tolist()

# Create a copy of the dataframe
df2= df.copy()

# Iterate until an optimal solution is found or the list of subjects is empty
while sorted_subjects:
    result = optimize_threshold(df2, subjects_info, min_timepoints=505, 
                                min_controls=20, min_patients=20, percentage=0.15)
    
    if result is not None:
        optimal_thr, optimal_subjects = result
        print(f"Optimal threshold: {optimal_thr}")
        print(f"Subjects to keep: {optimal_subjects}")
        break
    else:
        # Remove the first subject from the dataframe
        df2 = df2.drop(columns=[sorted_subjects[0]])
        
        # Remove the first subject from the list
        sorted_subjects.pop(0)

if not sorted_subjects:
    print("No optimal solution found after removing all subjects.")

with open(f'/m/cs/scratch/networks-pm/epeli/subject_scrub_fd{str(optimal_threshold)}.txt', 'w') as f:
    for line in sub_list:
        f.write(f"{line}\n")

########################### Visualize optimal solution ########################

# Plot for each participant to check the quality
cmap = sns.color_palette("Greys", as_cmap=True)
cmap.set_bad(color='red')

df_plot = df[optimal_subjects]
#df_plot = df_plot.where(df_plot <= optimal_thr) # For hard scrub
#df_plot.loc[df_plot.isnull().any(axis=1),:] = np.nan # For hard scrub
df_plot = df_plot.where((df_plot > optimal_thr).mean(axis=1) <= 0.15) #adjust the percent accordingly


fig, axs = plt.subplots(1,1,figsize=(10, 10))
sns.heatmap(df_plot.T, cmap=cmap, vmin=0, vmax=0.5, xticklabels=False, yticklabels=True, ax=axs)
axs.set_ylabel("subject")
axs.set_xlabel("TR")
axs.set_title(f'scrubbing for {str((subjects_info.loc[optimal_subjects, "group"] == 1.0).sum())} TC and {str((subjects_info.loc[optimal_subjects, "group"] == 2.0).sum())} ADHD for FD<{str(optimal_thr)}. Remaining TRs:{str(len(df_plot)-df_plot["sub-F001"].isna().sum())}')

# Add vertical lines
axs.axvline(x=235, color='blue', linewidth=2)
axs.axvline(x=435, color='blue', linewidth=2)
axs.axvline(x=635, color='blue', linewidth=2)

#plt.show()
plt.savefig(f'{path}/tc-{str((subjects_info.loc[optimal_subjects, "group"] == 1.0).sum())}_adhd-{str((subjects_info.loc[optimal_subjects, "group"] == 2.0).sum())}_thr-{str(optimal_thr)}.pdf')

########################## Check the discarded subjects #######################
discarded_subjects = subjects_info[~subjects_info.index.isin(optimal_subjects)]
