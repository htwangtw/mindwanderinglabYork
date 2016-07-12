'''
set working directory 
i.e.
WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'
'''

WD = 'U:\\Project_CCA'

'''
set result output directory 
i.e.
resultdir = 'U:\\Project_CCA\\results'
'''

resultdir = 'U:\\Project_CCA\\Results\\TS_txt'

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
roiLabel = 'U:\\Project_CCA\\Masks\\Bzdok_DMN14_lables.nii.gz'

'''

roiLabel = 'U:\\Project_CCA\\Masks\\Bzdok_DMN14_lables.nii.gz'

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

scca_rs_weights_keys = 'U:\\Project_CCA\\Results\\cs_cross_corr_Bzdok_DMN14_keys.npy'

'''
SCCA image weights npy file
It should be a npy file.
If you had run scca_output.py, the file should have been created automatically.
It should be a matrix of number of components by number of ROI pairs 

i.e.
scca_rs_weights = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'
'''

scca_rs_weights = 'U:\\Project_CCA\\Results\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'

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

#average all comps lodaings
def mean_nonzero(data, a):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        temp_sum = np.sum(data!=0, axis=a)
        # temp_sum [temp_sum==0] = 1 
        output = np.sum(data, axis=a)/temp_sum
        output[np.isnan(output)] = 0
    return output

ave_loadings_flat = mean_nonzero(rest_loading,1)
ave_loadings_mat = np.zeros((14,14))
ave_loadings_mat[idx] = ave_loadings_flat
ave_loadings_mat = ave_loadings_mat + ave_loadings_mat.T
ave_loadings = mean_nonzero(ave_loadings_mat, 1)

ts_len = masker.transform(rs_niis[0]).shape[0]
for i_rs_img, rs_img in enumerate(rs_niis):
    par = '_'.join(rs_img.split(os.sep)[-1].split('_')[0:2])
    outputDIR = resultdir + '_new' + os.sep + par
    if not os.path.exists(outputDIR):
        os.makedirs(outputDIR)
    print('%i/%i: %s' %(i_rs_img + 1, len(rs_niis),par))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        rs_reg_ts = masker.transform(rs_img)
    #weighted TS of the average
    cur_all_weightedTS = mean_nonzero(rs_reg_ts*ave_loadings, 1)
    cur_all_txtfn = outputDIR + os.sep + '%s_weightedTS_%s_allcomps.txt' %(par, analysis_name)
    np.savetxt(cur_all_txtfn, cur_all_weightedTS, fmt='%f',)
    for i_comp in range(rest_loading.shape[1]):
        cur_loadings = rest_loading[np.where(rest_loading[:,i_comp]!=0),i_comp].flatten()
        cur_keys = loading_labels[np.where(rest_loading[:,i_comp]!=0)] #sanity check
        cur_x_idx = idx[0][np.where(rest_loading[:,i_comp]!=0)]
        cur_y_idx = idx[1][np.where(rest_loading[:,i_comp]!=0)]
        cur_weighted_ts = np.zeros((ts_len))
        for i_corr in range(len(cur_loadings)):
            cur_weighted_ts += (rs_reg_ts[:,cur_x_idx[i_corr]]+rs_reg_ts[:,cur_y_idx[i_corr]])*cur_loadings[i_corr]
            cur_par_txtfn = outputDIR + os.sep + '%s_weightedTS_%s_comp-%i.txt' %(par, analysis_name, i_comp + 1)
        np.savetxt(cur_par_txtfn, cur_weighted_ts/len(cur_loadings), fmt='%f',)


