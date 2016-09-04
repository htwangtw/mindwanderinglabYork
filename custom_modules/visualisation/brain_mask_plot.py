import glob, os, sys
import numpy as np
from nilearn.image import resample_img, index_img
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

roiLabel = 'Bzdok_DMN14_lables.nii.gz'
label_atlas_nii= nib.load(roiLabel)
