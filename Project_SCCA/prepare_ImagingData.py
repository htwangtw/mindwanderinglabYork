DATA_DIR = 'U:\\PhDProjects\\CS_Analysis\\CS_brain_preprocessed'
ATLAS_DIR = 'U:\\PhDProjects\\Project_CCA\\Yeo15_DMN_6ROIs\\*.nii'
roiLabel = 'U:\\PhDProjects\\Project_CCA\\Yeo15_DMN_6ROIs\\Yeo15_DMN_6ROIs_lables.nii.gz'
crosscorr = 'cs_cross_corr_Yeo15_DMN_6ROIs'
#########################################################################################
import glob
import os
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

rs_niis = glob.glob(DATA_DIR + os.sep + '*.nii.gz')
tmp_nii_path = rs_niis[0]
tmp_nii = nib.load(tmp_nii_path)

if ATLAS_DIR.split('.')[-1]== 'nii':
    RE_ATLAS_DIR = ATLAS_DIR + '.gz'
    fform = '.nii'
elif ATLAS_DIR.split('.')[-1]== '.gz':
    RE_ATLAS_DIR = ATLAS_DIR
    fform = '.nii.gz'
else:
    print 'You are not loading NIFTI files'


atlas_nii = glob.glob(ATLAS_DIR)
atlas_names = [roi.split(os.sep)[-1].split(fform)[0]  for roi in atlas_nii]
atlas_names = np.array(atlas_names)

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
elif ATLAS_DIR.split('.')[-1]== '.gz':
    pass
else:
    print 'You are not loading NIFTI files'

atlas_re_nii = glob.glob(RE_ATLAS_DIR)


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
# #load saved labels
# label_atlas_nii= nib.load('DMN_subregions_label.nii.gz')

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

    #for sanity check: if the data is ordered in participant number
    corr_ID = int(rs_img.split(os.sep)[-1].split('_')[0])
    ind_list.append(corr_ID-1)

corr_mat_vect_array = np.array(corr_mat_vect_list)
#sanity check
corr_mat_vect_array_order = np.zeros(corr_mat_vect_array.shape)
corr_mat_vect_array_order[ind_list,:] = corr_mat_vect_array[:,:]
print(corr_mat_vect_array_order.shape)

np.save(crosscorr, corr_mat_vect_array_order)

reg_reg_names = [atlas_names[a] + ' vs ' + atlas_names[b] for (a,b) in zip(triu_inds[0], triu_inds[1])]

np.save(crosscorr+'_keys', reg_reg_names)
