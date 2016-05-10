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
rest_comp [np.isnan(rest_comp)] = 0
#load ROI masks
ATLAS_DIR = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_smoothed_DMN_subregions\\*fwhm8.nii.gz'
# ATLAS_DIR = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN\\*.nii.gz'
atlas_nii = sorted(glob.glob(ATLAS_DIR)) #windows
binarize = False

# matching filenames
atlas_nii_re = []
atlas_nii_re.append(atlas_nii[0:2])
atlas_nii_re.append(atlas_nii[5:11])
atlas_nii_re.append(atlas_nii[2:5])
atlas_nii_re.append(atlas_nii[11:])
atlas_nii = [item for sublist in atlas_nii_re for item in sublist]


sample_nii = nib.load('U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed\\001_R4087_MNI152_2mm_prepro_filtered_func_data.nii.gz')
weight_atlas = np.zeros(sample_nii.shape[:3])

for k in range(rest_comp.shape[1]):
# for k in range(2):
	print 'component %i'%(k+1)
	weight_atlas = np.zeros(sample_nii.shape[:3])
	for i_roi, cur_roi in enumerate(atlas_nii):
		print i_roi+1, cur_roi.split(os.sep)[-1].split('.nii.gz')[0], rest_comp[i_roi,k]
		cur_re_lable = resample_img(
	            img=cur_roi,
	            target_affine=sample_nii.get_affine(),
	            target_shape=sample_nii.shape[:3],
	            interpolation='nearest'
	        )
		cur_data = cur_re_lable.get_data()
		if binarize:
			cur_data = np.array(cur_data > 0.5, dtype=np.int)
		if len(cur_data.shape) > 3:
			cur_data = cur_data[:, :, :, 0]
		if cur_data.max()>1:
			cur_data /= cur_data.max()
		weight_atlas += cur_data * rest_comp[i_roi,k]
		print np.sum(cur_data * rest_comp[i_roi,k])
	#create labels
	weight_atlas_nii = nib.Nifti1Image(
	    weight_atlas,
	    affine=sample_nii.get_affine(),
	    header=sample_nii.get_header()
	)
	weight_atlas_nii.to_filename('weightedmasks\\smoothed_weightedmask_comp%i.nii.gz'%(k+1))


