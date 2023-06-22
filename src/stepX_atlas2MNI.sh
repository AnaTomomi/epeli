#!/bin/bash


module load fsl
source $FSLDIR/etc/fslconf/fsl.sh

ref=/m/cs/scratch/networks-pm/atlas/MNI_templates/MNI152_T1_2mm_mask.nii.gz
file=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/HaskinsPeds_NL_template_3x3x3_maskRESAMPLED.nii
atlas_file=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/four.nii
new_file=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/four2mm.nii
matrix=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/MNI2mm_matrix.mat

flirt -in ${file} -ref ${ref} -omat ${matrix} -bins 256 -cost corratio -searchrx -120 120 -searchry -120 120 -searchrz -120 120 -dof 9 

flirt -in ${atlas_file} -applyxfm -init ${matrix} -out ${new_file} -paddingsize 0.0 -interp trilinear -ref ${ref}

gunzip -d ${new_file}.gz

