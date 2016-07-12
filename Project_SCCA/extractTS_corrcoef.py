
'''
SCCA image ROI pairs npy file
It should be a npy file.
If you had run prepare_ImageData.py, the file should have been created automatically.
It should be a vector of names of ROI pairs.
i.e.
scca_rs_weights_keys = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\cs_cross_corr_Bzdok_DMN14_keys.npy'
'''

scca_rs_weights_keys = 'U:\\PhDProjects\\Project_CCA\\Results\\cs_cross_corr_Bzdok_DMN14_keys.npy'

'''
SCCA image weights npy file
It should be a npy file.
If you had run scca_output.py, the file should have been created automatically.
It should be a matrix of number of components by number of ROI pairs 

i.e.
scca_rs_weights = 'C:\\Users\\hw1012\\Documents\\Project_CCA\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'
'''

scca_rs_weights = 'U:\\PhDProjects\\Project_CCA\\Results\\RSxMWQ_cross_corr_Bzdok_DMN14_SCCAloading.npy'

'''
Cross corelation coefficient 
'''
rscorrfn = 'U:\\PhDProjects\\Project_CCA\\Results\\cs_cross_corr_Bzdok_DMN14.npy'
'''

Options completed.
---------------------------------------------------------------------
'''

from os.path import expanduser
import glob, os, sys, warnings
rest_loading = np.load(expanduser(scca_rs_weights)) 
loading_labels = np.load(expanduser(scca_rs_weights_keys))
rest_data = np.load(expanduser(rscorrfn))
rest_data[np.isnan(rest_data)] = 1

