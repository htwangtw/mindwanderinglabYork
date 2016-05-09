"""
Time series preprocessing for CCA and other stuff (potentially)

Created on Wed 24 Feb 13:43:09 2016
Last updated on Wed 20th of Apr 2016

@author: Danilo Bzdok; mentained by Haoting

Please ensure the following packages are installed if you are running on your personal machine:
	numpy, nilearn, nibable

The atlas directory should include the .nii and/or the .nii.gz files of ROIs only.

If you are using the preprocessed data for Sparse-CCA:
	-The id should match the subject id of the imaging data or the other set of behavioral data.
	-In other words, the same participant should have the same id across those two set of data.

"""

WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN'
DATA_DIR = 'U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed'
# ATLAS_DIR = 'U:\\PhDProjects\\Project_CCA\\Bzdok_DMN\\*.nii'
keep the atlas folder clean is a good idea
roiLabel = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\Bzdok_DMN14_lables.nii.gz'
#name: [project]_cross_corr_[chosen masks][number of the regions]
crosscorr = 'cs_cross_corr_Bzdok_DMN14_P165'

#########################################################################################
import glob, os, sys
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

os.chdir(WD)
#rs_niis = glob.glob(DATA_DIR + os.sep + '*.nii.gz')
rs_niis = sorted(glob.glob(DATA_DIR + os.sep + '*.nii.gz')) #windows
tmp_nii_path = rs_niis[0]
tmp_nii = nib.load(tmp_nii_path)

if ATLAS_DIR.split('.')[-1]== 'nii':
    RE_ATLAS_DIR = ATLAS_DIR + '.gz'
    fform = '.nii'
elif ATLAS_DIR.split('.')[-1]== 'gz':
    RE_ATLAS_DIR = ATLAS_DIR
    fform = '.nii.gz'
else:
	fform = ATLAS_DIR.split('.')[-1]
	sys.exit('You are not loading NIFTI files, it was .%s' %fform)

# atlas_nii = glob.glob(ATLAS_DIR)
atlas_nii = sorted(glob.glob(ATLAS_DIR)) #windows
atlas_names = [roi.split(os.sep)[-1].split(fform)[0]  for roi in atlas_nii]
atlas_names = np.array(atlas_names)
np.save(crosscorr+'_ROIS', atlas_names)

if ATLAS_DIR.split('.')[-1]== 'nii':
    re_atlas_nii = []
    for cur_roi in atlas_nii:
        # reshape the data (put the mask on the particiapnt's data, matching the coordinates and shapes)
        re_cur_roi = resample_img(
            img=cur_roi,
            target_affine=tmp_nii.get_affine(),
            target_shape=tmp_nii.shape[:3],
            interpolation='nearest'
        )
        
        # binarize the data
        cur_data = re_cur_roi.get_data()
        cur_data_bin = np.array(cur_data > 0.5, dtype=np.int)
        re_cur_roi = nib.Nifti1Image(
            cur_data_bin,
            affine=tmp_nii.get_affine(),
            header=tmp_nii.get_header()
        )
        
        # dump to disk
        re_cur_roi.to_filename(cur_roi + '.gz')
else:
    pass


#atlas_re_nii = glob.glob(RE_ATLAS_DIR)
atlas_re_nii = sorted(glob.glob(RE_ATLAS_DIR))  #windows
if len(atlas_re_nii) != len(atlas_nii):
	sys.exit('''You are not loading the correct .nii.gz files to create masks.
	Check if atlas_re_nii and atlas_nii matches.''')
else:
	print 'ok'

# parse the time series from our atlas
label_atlas = np.zeros(tmp_nii.shape[:3], dtype=np.int)
for i_roi, roi in enumerate(atlas_re_nii):
    cur_roi_data = nib.load(roi).get_data()
    if len(cur_roi_data.shape) > 3:
        cur_roi_data = cur_roi_data[:, :, :, 0]
    label_atlas[cur_roi_data > 0.1] = i_roi + 1


#create labels
label_atlas_nii = nib.Nifti1Image(
    label_atlas,
    affine=tmp_nii.get_affine(),
    header=tmp_nii.get_header()
)

#save for future usage
label_atlas_nii.to_filename(roiLabel)
#load saved labels
# label_atlas_nii= nib.load(roiLabel)

masker = NiftiLabelsMasker(labels_img=label_atlas_nii, standardize=True,
                           memory='nilearn_cache', verbose=0)
masker.fit()

corr_mat_vect_list = []
ind_list = []


for i_rs_img, rs_img in enumerate(rs_niis):
    print('%i/%i: %s' % (i_rs_img + 1, len(rs_niis), rs_img))
    rs_reg_ts = masker.transform(rs_img)

    corr_mat = np.corrcoef(rs_reg_ts.T)
    triu_inds = np.triu_indices(corr_mat.shape[0], 1)
    corr_mat_vect = corr_mat[triu_inds]
    # save for later
    corr_mat_vect_list.append(corr_mat_vect)
corr_mat_vect_array = np.array(corr_mat_vect_list)

print(corr_mat_vect_array.shape) 

if len(corr_mat_vect_array) == label_atlas_nii.shpae[0]:
	print corr_mat_vect_array.shape
	np.save(crosscorr, corr_mat_vect_array)
else:
	sys.exit('The shpae should be %i by %i. Check the .nii.gz files in your atlas directory.' 
		%(len(rs_niis), label_atlas_nii.shpae[0]))

reg_reg_names = [atlas_names[a] + ' vs ' + atlas_names[b] for (a,b) in zip(triu_inds[0], triu_inds[1])]
np.save(crosscorr+'_keys', reg_reg_names)