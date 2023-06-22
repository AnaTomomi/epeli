%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Compute the ISC permutation tests for the EPELI data                    %
%                                                                         %
% author: trianaa1                                                        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
close all
clc

addpath(genpath('/m/cs/scratch/networks-pm/epeli/ISCstats'));

%Load the data 
atlas = 'seitzman';
data = load(sprintf('/m/cs/scratch/networks-pm/epeli/data/isc/all_%s.mat',atlas));
G1_all = data.data;

%Define the parameters
n_rois = size(G1_all,3);
n_per = 5000;
NG1 = size(G1_all,2);

%Make the behavioral ISC
behav = xlsread(sprintf('/m/cs/scratch/networks-pm/epeli/data/isc/behavioral_%s.xlsx',atlas));
behdata = corr(behav);

% loop over the different ROIs
results = zeros(n_rois,2);
for i=1:n_rois
    G1 = G1_all(:,:,i);
    iscdata = corr(G1); % isc matrix with within group and across groups ISC
    [r p]=iscstats_mantel(iscdata,behdata,n_per,'spearman'); %Mantel test
    results(i,1) = r;
    results(i,2) = p;
    disp(i)
end

save(sprintf('/m/cs/scratch/networks-pm/epeli/results/isc/mantel_%s.mat',atlas),'results')

%Correct for multiple comparisons
q = mafdr(results(:,2),'BHFDR','true');
