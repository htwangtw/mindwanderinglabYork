#load the weighted*ROIcorr
import glob, os, sys
from os.path import expanduser
import nibabel as nib
from nilearn.image import resample_img, index_img
import numpy as np

WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'
os.chdir(WD)

rest_loading = np.load(expanduser('RSxMWQ_RS_SCCAloading_mat.npy'))
# rest_comp = np.sum(rest_loading, axis=1)
rest_comp = np.sum(rest_loading, axis=1)/np.sum(rest_loading!=0, axis=1)
rest_comp[np.isnan(rest_comp)] = 0
#load ROI masks
ATLAS_DIR = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_smoothed_DMN_subregions\\*.nii.gz'
atlas_nii = sorted(glob.glob(ATLAS_DIR)) #windows
sample_nii = nib.load('U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed\\001_R4087_MNI152_2mm_prepro_filtered_func_data.nii.gz')
weight_atlas = np.zeros(sample_nii.shape[:3])

for k in range(rest_comp.shape[1]):
	print 'component %i'%(k+1)
	for i_roi, cur_roi in enumerate(atlas_nii):
		print i_roi+1, cur_roi.split(os.sep)[-1].split('.nii.gz')[0], rest_comp[i_roi,k]
		# binarize the data
		cur_re_lable = resample_img(
	            img=cur_roi,
	            target_affine=sample_nii.get_affine(),
	            target_shape=sample_nii.shape[:3],
	            interpolation='nearest'
	        )
		cur_data = cur_re_lable.get_data()
		cur_data_bin = np.array(cur_data > 0.5, dtype=np.int)
		cur_data = nib.load(cur_roi).get_data()
		if len(cur_data.shape) > 3:
			cur_data = cur_data[:, :, :, 0]
		weight_atlas[cur_data > 0.1] = rest_comp[i_roi,k]

	#create labels
	weight_atlas_nii = nib.Nifti1Image(
	    weight_atlas,
	    affine=sample_nii.get_affine(),
	    header=sample_nii.get_header()
	)
	weight_atlas_nii.to_filename('weightedmask_comp%i.nii.gz'%(k+1))


