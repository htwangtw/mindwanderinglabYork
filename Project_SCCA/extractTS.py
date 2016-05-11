'''
set working directory 
i.e.
WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'
'''

WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'

'''
set result output directory 
i.e.
resultdir = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\results'
'''

resultdir = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\TS_txt'

'''
set preprocessed participant data directory 
i.e.
DATA_DIR = 'U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed'
'''

DATA_DIR = 'U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed'

'''
ROI Label nifti file
It should be a nifti file with ROIs labeled.
If you had run prepare_ImageData.py, the file should have been created automatically.

i.e.
roiLabel = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN14_lables.nii.gz'

'''

roiLabel = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN14_lables.nii.gz'

'''
the number of ROIs used in prepare_ImageData.py.

i.e.
n_ROIs = 14
'''

n_ROIs = 14

'''
SCCA image ROI pairs npy file
It should be a npy file.
If you had run prepare_ImageData.py, the file should have been created automatically.
It should be a vector of names of ROI pairs.
i.e.
scca_rs_weights_keys = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\cs_cross_corr_Bzdok_DMN14_keys.npy'
'''

scca_rs_weights_keys = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\cs_cross_corr_Bzdok_DMN14_keys.npy'

'''
SCCA image weights npy file
It should be a npy file.
If you had run scca_output.py, the file should have been created automatically.
It should be a matrix of number of components by number of ROI pairs 

i.e.
scca_rs_weights = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'
'''

scca_rs_weights = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'

'''

Options completed.
---------------------------------------------------------------------

'''
from os.path import expanduser
import glob, os, sys, warnings
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib

os.chdir(WD)

rs_niis = sorted(glob.glob(DATA_DIR + os.sep + '*.nii.gz'))# participants
analysis_name = scca_rs_weights.split(os.sep)[-1].split('.')[0]
label_atlas_nii= nib.load(roiLabel) 
rest_loading = np.load(expanduser(scca_rs_weights)) 
loading_labels = np.load(expanduser(scca_rs_weights_keys))
idx = np.triu_indices(n_ROIs, 1)

from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=label_atlas_nii, standardize=True,
                           memory='nilearn_cache', verbose=0)
masker.fit()

ts_len = masker.transform(rs_niis[0]).shape[0]
for i_comp in range(rest_loading.shape[1]):
    print('***Component %i/%i started. ***' %(i_comp+1, rest_loading.shape[1]))
    cur_loadings = rest_loading[np.where(rest_loading[:,i_comp]!=0),i_comp].flatten()
    cur_keys = loading_labels[np.where(rest_loading[:,i_comp]!=0)] #sanity check
    cur_x_idx = idx[0][np.where(rest_loading[:,i_comp]!=0)]
    cur_y_idx = idx[1][np.where(rest_loading[:,i_comp]!=0)]
    cur_weighted_ts_comp = np.zeros((ts_len, len(cur_loadings), len(rs_niis)))
    for i_rs_img, rs_img in enumerate(rs_niis): #number of subjects
        print('%i/%i: %s' %(i_rs_img + 1, len(rs_niis),rs_img))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            rs_reg_ts = masker.transform(rs_img)
        par = rs_img.split(os.sep)[-1].split('MNI')[0]    
        for i_corr in range(len(cur_loadings)):
            print('%i/%i component %i: %i/%i - %s' 
                %(i_rs_img + 1, len(rs_niis), 
                    i_comp + 1, i_corr + 1, len(cur_loadings), cur_keys[i_corr]))
            cur_weighted_ts = rs_reg_ts[:,cur_x_idx[i_corr]]*rs_reg_ts[:,cur_y_idx[i_corr]]*cur_loadings[i_corr]
            cur_weighted_ts_comp[:,i_corr, i_rs_img]  = cur_weighted_ts
        cur_par_txtfn = resultdir + os.sep + '%sweightedTS_%s_comp-%i.txt' %(par, analysis_name, i_comp + 1)
        np.savetxt(cur_par_txtfn, cur_weighted_ts_comp[..., i_rs_img], fmt='%f',)
    print('***Component %i/%i finished. ***' %(i_comp+1, rest_loading.shape[1]))
    np.save(resultdir + os.sep + 'weightedTS_%s_comp-%i' %(analysis_name, i_comp + 1), cur_weighted_ts_comp)
print('Job done!')