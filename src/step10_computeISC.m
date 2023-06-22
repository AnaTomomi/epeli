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
data = load(sprintf('/m/cs/scratch/networks-pm/epeli/data/isc/tc_%s.mat',atlas));
G1_all = data.data;
data = load(sprintf('/m/cs/scratch/networks-pm/epeli/data/isc/adhd_%s.mat',atlas));
G2_all = data.data;

%Define the parameters
n_rois = size(G1_all,3);
n_per = 10000;
NG1 = size(G1_all,2);
NG2 = size(G2_all,2);

% loop over the different ROIs
results = zeros(n_rois,2);
for i=1:n_rois
    G1 = G1_all(:,:,i);
    G2 = G2_all(:,:,i);
    iscdata = corr([G1 G2]); % isc matrix with within group and across groups ISC
    out = iscstats_ttest2_np(iscdata,[ones(1,NG1) 2*ones(1,NG2)],n_per);
    results(i,1) = out.tval;
    results(i,2) = out.pval;
    disp(i)
end

save(sprintf('/m/cs/scratch/networks-pm/epeli/results/isc/gc_%s.mat',atlas),'results')

%Correct for multiple comparisons
q = mafdr(results(:,2),'BHFDR','true');
