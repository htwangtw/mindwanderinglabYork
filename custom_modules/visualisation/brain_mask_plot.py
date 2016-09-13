import glob, os, sys
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

roiLabel = 'Bzdok_DMN14_lables.nii.gz'
label_atlas_nii= nib.load(roiLabel)

# First plot the map for the PCC: index 4 in the atlas

display = plotting.plot_roi(label_atlas_nii,
								 cut_coords=(9,66,21),
                                 colorbar=False,
                                 vmin=1, vmax=14,
                                 title="Selected DMN ROIs",
                                 draw_cross=False)
plotting.show()