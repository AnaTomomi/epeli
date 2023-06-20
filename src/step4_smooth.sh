#!/bin/bash
#SBATCH -p batch
#SBATCH -t 00:15:00
#SBATCH --qos=normal
#SBATCH --mem-per-cpu=5G
#SBATCH --array=0-65

module load fsl/5.0.9
source $FSLDIR/etc/fslconf/fsl.sh

n=$SLURM_ARRAY_TASK_ID
number=`sed "${n}q;d" subjects.txt`
FWHM=2.5532 #This number is FWHM/2.35

file=/m/cs/scratch/networks-pm/epeli/data/organized_videos/${number}/${number}_task-mergedvideoupsampled-denoised-24HMP-8Phys_HPF.nii
out_file=/m/cs/scratch/networks-pm/epeli/data/organized_videos/${number}/${number}_task-mergedvideoupsampled-denoised-24HMP-8Phys_HPF_smoothed6mm.nii

fslmaths ${file} -kernel gauss $FWHM -fmean ${out_file}

gunzip -d ${out_file}.gz #decompress
