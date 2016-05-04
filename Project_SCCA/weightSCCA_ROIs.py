#load the weighted*ROIcorr

#load ROI masks
import nibabel as nib
atlas_nii = sorted(glob.glob(ATLAS_DIR)) #windows

#load lables so we can call the masks acordingly

#print of the weighted*ROIcorr, should be size(n_sbj, n_corr)
#average the weighted*ROIcorr by column

#multiply the weighted*ROIcorr with the masks, create nifit files (n = non-zero)


