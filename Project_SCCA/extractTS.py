WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'
DATA_DIR = 'U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed'
roiLabel = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN14_lables.nii.gz'

from os.path import expanduser

import glob, os, sys
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

os.chdir(WD)
# participants
rs_niis = sorted(glob.glob(DATA_DIR + os.sep + '*.nii.gz'))
# the label file created by 'prepare_ImagingData.py'
label_atlas_nii= nib.load(roiLabel) 
# SCCA latent component loadings: brain (the number of ROI pairs* the number of components)
rest_loading = np.load(expanduser('RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy')) 
# keys: ROI pairs, for sanity check
loading_labels = np.load(expanduser('cs_cross_corr_Bzdok_DMN14_keys.npy'))
# get the index of the ROI-pairs
idx = np.triu_indices(14, 1)

masker = NiftiLabelsMasker(labels_img=label_atlas_nii, standardize=True,
                           memory='nilearn_cache', verbose=0)
masker.fit()

for i_comp in range(rest_loading.shape[1]): #6 components
# for i_comp in range(1):
    print('***Component %i started. ***' %(i_comp + 1))
    cur_loadings = rest_loading[np.where(rest_loading[:,i_comp]!=0),i_comp].flatten()
    cur_keys = loading_labels[np.where(rest_loading[:,i_comp]!=0)] #sanity check
    cur_x_idx = idx[0][np.where(rest_loading[:,i_comp]!=0)]
    cur_y_idx = idx[1][np.where(rest_loading[:,i_comp]!=0)]
    cur_weighted_ts_comp = np.zeros((len(cur_loadings), len(rs_reg_ts), len(rs_niis)))
    for i_rs_img, rs_img in enumerate(rs_niis): #number of subjects
        print('%i/%i: %s' %(i_rs_img + 1, len(rs_niis),rs_img))
        rs_reg_ts = masker.transform(rs_img)      
        for i_corr in range(len(cur_loadings)):
            print('%i/%i component %i: %i/%i - %s' 
                %(i_rs_img + 1, len(rs_niis), 
                    i_comp + 1, i_corr + 1, len(cur_loadings), cur_keys[i_corr]))
            cur_weighted_ts = rs_reg_ts[:,cur_x_idx[i_corr]]*rs_reg_ts[:,cur_y_idx[i_corr]]*cur_loadings[i_corr]
            cur_weighted_ts_comp[i_corr, :, i_rs_img]  = cur_weighted_ts
    print('***Component %i finished. ***' %(i_comp+1))
    np.save('weightedTS_comp%i' %(i_comp + 1), cur_weighted_ts_comp)
print('Job done!')