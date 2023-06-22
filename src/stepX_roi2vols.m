clear all
close all
clc

addpath('/m/cs/scratch/networks-pm/software/NIFTI');

nii = load_untouch_nii('/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/HaskinsPeds_NL_atlasRESAMPLED1.0.nii');
n_rois = 107;

new_data=zeros([size(nii.img) n_rois]);
data = nii.img;

for i=1:n_rois;
    ids = find(data==i);
    data1 = zeros(size(nii.img));
    data1(ids) = i;
    new_data(:,:,:,i) = data1;
end

nii.hdr.dime.dim(1) =4;
nii.hdr.dime.dim(5) =n_rois;

nii.img = uint8(new_data);

save_untouch_nii(nii,'/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/four.nii');