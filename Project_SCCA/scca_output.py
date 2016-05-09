n_components = 6
pen_brain = 0.3
pen_behave = 0.5

WD = 'C:\\Users\\hw1012\\Documents\\Project_CCA'
'''
the included behavioural data should include only the variables/tasks/participants
you are looking at in this analysis.
The first column of your behavioural data must be participant number.

behavior participant number should be smaller than or equal to rs participant number.
ie. we have the RS data up to P145, the last participant you include should be P145 as well.
'''
beh_keysfn = 'Master_keys_MWQ.npy'
behavefn = 'data_MWQ_task.npy' 

n_areas = 14
rscorrfn = 'cs_cross_corr_Bzdok_DMN14_P165.npy'
corr_keys_fn = 'cs_cross_corr_Bzdok_DMN14_keys.npy'
region_labels_fn = 'cs_cross_corr_Bzdok_DMN14_ROIS.npy'
result_corr_fn = 'BzdokDMN14_MWQ_CRT_penBrain%1.1f_penBehav%1.1f_nComponets%1.0f.pdf' %(pen_brain, pen_behave, n_components)

import pandas.rpy.common as com
# load the Stanford package for SCCA, it should load dependent packages as well
# please change the path.
com.r(
    '''
    library(plyr, lib.loc='U:/My Documents/R/win-library/3.2')
    library(impute, lib.loc='U:/My Documents/R/win-library/3.2')
    library(Rcpp, lib.loc='U:/My Documents/R/win-library/3.2')
    library(PMA, lib.loc='U:/My Documents/R/win-library/3.2')
    ''')


###################################################################################################
from os.path import expanduser

from joblib import load
import numpy as np
import matplotlib.pyplot as plt

import readline
import rpy2.rinterface as ri
import pandas as pd

#set cd here
import os
os.chdir(WD)


#load data

all_keys = np.load(expanduser(beh_keysfn))
all_behavioral_data = np.load(expanduser(behavefn))
rest_data = np.load(expanduser(rscorrfn))


subject_subset = all_behavioral_data[:, 0].astype('i4') - 1
keys = all_keys[1:]
behavioral_data = all_behavioral_data[:, 1:14]

X = rest_data[subject_subset]
Y = behavioral_data
#demean
S = Y.sum(axis=0) / Y.shape[0]
Y -= S[np.newaxis, :]
var = (Y ** 2).sum(axis=0)
var[var == 0] = 1
Y /= var
X[np.isnan(X)] = 1

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
    """ % (n_components, pen_brain, pen_behave))


# convert the results back to dataframes and then to numpy arrays
df_u = com.convert_robj(com.r('out[1]'))['u']
df_v = com.convert_robj(com.r('out[2]'))['v']

x_loadings = df_u.as_matrix()
y_loadings = df_v.as_matrix()


#main output
idx = np.triu_indices(n_areas, 1)
corr_mat = np.zeros((n_areas, n_areas, n_components))

for i in range(n_components):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, i]
    corr_mat[..., i] = this_mat + this_mat.T


region_labels = np.load(expanduser(region_labels_fn))
fig = plt.figure(figsize=(20, 40))
fig.subplots_adjust(left=0.3, right=0.8, hspace = 0.4)
for i in range(n_components):
    ax = fig.add_subplot(n_components, 2, i*2 + 1)
    brain = ax.matshow(corr_mat[..., i], vmin=-1, vmax=1,
               cmap=plt.cm.RdBu_r)
    ax.set_xticks(np.arange(n_areas))
    ax.set_xticklabels(region_labels, rotation=90)
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(region_labels)
    # cb_brain = fig.colorbar(brain)

    behav_ax = fig.add_subplot(n_components, 2, (i + 1)*2)
    behav_arr = np.zeros((len(keys),1))
    behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
    # behav = behav_ax.matshow(behav_arr, vmin=y_loadings[:, i].min(), vmax=y_loadings[:, i].max(),
    #                  cmap=plt.cm.RdBu_r)
    behav = behav_ax.matshow(behav_arr, vmin=-1, vmax=1,
                     cmap=plt.cm.RdBu_r)
    behav_ax.set_yticks(np.arange(len(keys)))
    behav_ax.set_yticklabels(keys)
    cb_behave = fig.colorbar(behav)

plt.savefig(result_corr_fn)
plt.close(fig)


comp = np.zeros((len(Y), y_loadings.shape[1]*2))
for i in range(y_loadings.shape[1]): 
	comp[:, i] = np.sum(X*x_loadings[:,i],1)
	comp[:, i+6] = np.sum(Y*y_loadings[:,i],1)
comp = np.column_stack((subject_subset+1, comp))
np.savetxt('foo4.csv', comp, fmt='%10.8f', delimiter=',')