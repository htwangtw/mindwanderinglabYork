n_components = 6
pen_brain = 0.3
pen_behave = 0.5
region_labels_fn = 'C:\\Users\\Hao-Ting\\Documents\\Work\\Project_CCA\\sourcedata\\data_cross_corr_Bzdok_DMN14_ROIS.npy'
beh_keysfn = 'C:\\Users\\Hao-Ting\\Documents\\Work\\Project_CCA\\sourcedata\\data_raw_keys_MWQ_master.npy'

behavefn = 'C:\\Users\\Hao-Ting\\Documents\\Work\\Project_CCA\\sourcedata\\Y_SCCAraw.npy'
rscorrfn = 'C:\\Users\\Hao-Ting\\Documents\\Work\\Project_CCA\\sourcedata\\X_SCCAraw.npy'

n_samples = 100

###################################################################################################
from os.path import expanduser
import numpy as np
from scca_r import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
#set cd here
import os


Y = np.load(expanduser(behavefn))
X = np.load(expanduser(rscorrfn))
penalty = (pen_brain,pen_behave)
data = (X, Y)

'''
define CCA
'''
import readline
import rpy2.rinterface as ri
import pandas as pd
import pandas.rpy.common as com
# load the Stanford package for SCCA, it should load dependent packages as well
# please change the path.
com.r(
'''
library(plyr)
library(impute)
library(Rcpp)
library(PMA)
''')

def SCCA_r(X,Y, n_components, pen):


	df_X = pd.DataFrame(X)
	df_Y = pd.DataFrame(Y)

	rmat_X = com.convert_to_r_matrix(df_X)
	rmat_Y = com.convert_to_r_matrix(df_Y)

	ri.globalenv['X'] = rmat_X
	ri.globalenv['Y'] = rmat_Y

	com.r(
	    """
	    out <- CCA(x = X, z = Y, K = %i, niter = 100, standardize = FALSE,
	               penaltyx = %f, penaltyz = %f)
	    """ % (n_components, pen[0], pen[1]))

	# convert the results back to dataframes and then to numpy arrays
	df_u = com.convert_robj(com.r('out[1]'))['u']
	df_v = com.convert_robj(com.r('out[2]'))['v']
	cors = com.convert_robj(com.r('out[16]'))['cors']

	x_loadings = df_u.as_matrix()
	y_loadings = df_v.as_matrix()
	cors = np.array(cors)
	
	loadings = (x_loadings, y_loadings)

	return loadings, cors

'''
Run CCA
'''
loadings, corr = SCCA_r(X, Y, n_components, penalty)

# '''
# bootstrap v1
# '''
# import scikits.bootstrap as boot
# def SCCA_boot(X,Y):
#     loadings = SCCA_r(X,Y, 6, penalty)
#     return loadings

# ci_test = boot.ci(data, statfunction=SCCA_boot, method='pi') 

'''
bootstrap v2
'''
# # testing
# X = np.random.rand(156*91).reshape(156,91)
# Y = np.random.rand(156*13).reshape(156,13)
# penalty = (0.5,0.3)
from numpy.random import randint
# select a random index
bootsInd = randint(X.shape[0],size=(n_samples, X.shape[0]))

for i, I in enumerate(bootsInd):
	cur_X = X[I,:]
	cur_Y = Y[I,:]
	cur_loadings, cur_cors = SCCA_r(cur_X,cur_Y, 6, penalty) # run SCCA

	if i ==0:
		# X_loadings_master = np.zeros((cur_loadings[0].shape[0], cur_loadings[0].shape[1], n_samples))
		# Y_loadings_master = np.zeros((cur_loadings[1].shape[0], cur_loadings[1].shape[1], n_samples))
		corr_master = np.zeros((cur_cors.shape[0], n_samples))
	# X_loadings_master[..., i] = cur_loadings[0] # save the component loadings
	# Y_loadings_master[..., i] = cur_loadings[1] # save the component loadings
	corr_master[..., i] = cur_cors.sum() #ref: Sugiyama el al. 2007


# confidnece interval
alpha = 0.05
ind_low = int(n_samples*alpha/2)
ind_high = int(n_samples - n_samples*alpha/2)

sort_corr_master = corr_master.sort()

ci_corr =  (sort_corr_master[ind_low], sort_corr_master[ind_high])

print('Sum of the correlation coefficient :' corr.sum())
print('Confident interval: 95%')
print('High:' ci_corr[0])
print('Low:' ci_corr[1])


