#!/bin/bash

module load fsl
source $FSLDIR/etc/fslconf/fsl.sh


#find the transformation matrix from Haskins to 2mm MNI
ref=/m/cs/scratch/networks-pm/atlas/MNI_templates/MNI152_T1_2mm.nii
file=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/HaskinsPeds_NL_template_3x3x3_maskRESAMPLED.nii
matrix=/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/Haskins_2mm_matrix.mat

flirt -in ${file} -ref ${ref} -omat ${matrix} -bins 256 -cost corratio -searchrx -120 120 -searchry -120 120 -searchrz -120 120 -dof 9 

#separate the ROIs into volumes
cd /m/cs/scratch/networks-pm/atlas/HaskinsPediatric/
mkdir -p haskins
for n in {0..107..1}; do 
	echo fslmaths HaskinsPeds_NL_atlasRESAMPLED1.0.nii -thr $n -uthr $n  AAL/$n".nii.gz"
	fslmaths HaskinsPeds_NL_atlasRESAMPLED1.0.nii -thr $n -uthr $n  AAL/$n".nii.gz"
done

# merge the files in one 4D vol
fslmaths merge -t
