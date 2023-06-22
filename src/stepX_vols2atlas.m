clear all
close all
clc

addpath('/m/cs/scratch/networks-pm/software/NIFTI');

nii = load_untouch_nii('/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/four2mm.nii');

SubROIs=nii;
[x y z v] = size(nii.img);
SubROIs.img=zeros(x,y,z,v);

%Assign only one region to each voxel ONLY
for i=1:x
    for j=1:y
        for k=1:z
            chosenROI=find(nii.img(i,j,k,:)==max(nii.img(i,j,k,:)));
            if size(chosenROI,1)==1
            SubROIs.img(i,j,k,chosenROI)=1;
            %SubROIs(i,j,k,chosenROI)=max(epi_STD(i,j,k,:));
            else
            SubROIs.img(i,j,k,chosenROI)=0; 
            end
        end
    end
end

% Merging the parcellation
for l=1:v
    SubROIs.img(:,:,:,l)=SubROIs.img(:,:,:,l)*l;
end

SubAtlas=zeros(x,y,z,1);
SubAtlas=sum(SubROIs.img,4);

SubROIs.hdr.dime.dim(1) =3;
SubROIs.hdr.dime.dim(5) =1;

SubROIs.img = uint8(SubAtlas);

save_untouch_nii(SubROIs,'/m/cs/scratch/networks-pm/atlas/HaskinsPediatric/Haskins2mm.nii');