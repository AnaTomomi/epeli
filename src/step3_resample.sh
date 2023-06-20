#!/bin/bash
#SBATCH -p batch
#SBATCH -t 01:20:00
#SBATCH --qos=normal
#SBATCH --mem-per-cpu=13G
#SBATCH --output=/m/cs/scratch/networks-pm/epeli/jobs/%a.out
#SBATCH --array=0-65


module load fsl
source $FSLDIR/etc/fslconf/fsl.sh

n=$SLURM_ARRAY_TASK_ID
number=`sed "${n}q;d" subjects.txt`

ref=/m/cs/scratch/networks-pm/atlas/MNI_templates/MNI152_T1_2mm.nii
file=/m/cs/scratch/networks-pm/epeli/data/organized_videos/${number}/${number}_task-mergedvideo-denoised-24HMP-8Phys_HPF.nii
new_file=/m/cs/scratch/networks-pm/epeli/data/organized_videos/${number}/${number}_task-mergedvideoupsampled-denoised-24HMP-8Phys_HPF.nii
matrix=/m/cs/scratch/networks-pm/epeli/data/organized_videos/${number}/${number}_matrix.mat

flirt -in ${file} -ref ${ref} -omat ${matrix} -bins 256 -cost corratio -searchrx -120 120 -searchry -120 120 -searchrz -120 120 -dof 9 

flirt -in ${file} -applyxfm -init ${matrix} -out ${new_file} -paddingsize 0.0 -interp trilinear -ref ${ref}

gunzip -d ${new_file}.gz

