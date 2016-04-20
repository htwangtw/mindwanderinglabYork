n_components = 5
pen_brain = 0.1
pen_behave = 0.3
SCCA_exp_var_check = False

WD = 'U:\\PhDProjects\\Project_CCA'
'''
the included behavioural data should be only the variables/tasks 
you are looking at in this analysis.
'''
# keysfn = 'select_keys_MWQ_mean.npy'
# behavefn = 'select_data_MWQ_mean.npy'
keysfn = 'select_keys_MWQ.npy'
behavefn = 'select_data_MWQ.npy' 

n_areas = 18
rscorrfn = 'cs_cross_corr_Bzdok_DMN18.npy'
corr_keys_fn = 'cs_cross_corr_Bzdok_DMN18_keys.npy'
region_labels_fn = 'cs_cross_corr_Bzdok_DMN18_ROIS.npy'
#format: [imaging data mask]_[behavioral data]_[penalty-brain]_[penalty-behavior](_othernotes).pdf
result_corr_fn = 'BzdokDMN_MWQpca_penBrain%1.1f_penBehav%1.1f_nComponets%1.0f.pdf' %(pen_brain, pen_behave, n_components)
result_brain_fn = 'BzdokDMN_MWQpca_penBrain%1.1f_penBehav%1.1f_nComponets%1.0f_RScorr.pdf' %(pen_brain, pen_behave, n_components)

# n_areas = 14
# rscorrfn = 'cs_cross_corr_Beth_Semantic14.npy'
# corr_keys_fn = 'cs_cross_corr_Beth_Semantic14_keys.npy'
# region_labels_fn = 'cs_cross_corr_Beth_Semantic14_ROIS.npy'

# #format: [imaging data mask]_[behavioral data]_[penalty-brain]_[penalty-behavior](_othernotes).pdf
# result_corr_fn = 'Beth_Semantic_MWQpca_penBrain%1.1f_penBehav%1.1f_nComponets%1.0f.pdf' %(pen_brain, pen_behave, n_components)
# result_brain_fn = 'Beth_Semantic_MWQpca_penBrain%1.1f_penBehav%1.1f_nComponets%1.0f_RScorr.pdf' %(pen_brain, pen_behave, n_components)

###################################################################################################
from os.path import expanduser

from joblib import load
import numpy as np
import matplotlib.pyplot as plt

import readline
import rpy2.rinterface as ri
import pandas.rpy.common as com
#panadas will not support this function in the future. 
#We need to find out how to use RPY2 to do the same thing
import pandas as pd

# load the Stanford package for SCCA, it should load dependent packages as well
com.r(
    '''
    library(plyr, lib.loc='U:/My Documents/R/win-library/3.2')
    library(impute, lib.loc='U:/My Documents/R/win-library/3.2')
    library(Rcpp, lib.loc='U:/My Documents/R/win-library/3.2')
    library(PMA, lib.loc='U:/My Documents/R/win-library/3.2')
    ''')

#set cd here
import os
os.chdir(WD)


#load data

keys = np.load(expanduser(keysfn))
behavioral_data = np.load(expanduser(behavefn))
#HT: MWQPCA
subjet_subset = behavioral_data[:, 0].astype('i4') - 1
keys = keys[5:]
behavioral_data = behavioral_data[:, 5:]
# #use these if you created the files correctly
# keys = keys[1:]
# behavioral_data = behavioral_data[:, 1:]

limit_exp_var = len(keys) #save for later

rest_data = np.load(expanduser(rscorrfn))

X = rest_data[subjet_subset]
Y = behavioral_data
#demean
S = Y.sum(axis=0) / Y.shape[0]
Y -= S[np.newaxis, :]
var = (Y ** 2).sum(axis=0)
var[var == 0] = 1
Y /= var
X[np.isnan(X)] = 1

#uncomment the next line if your computer fails to get environment variables


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
    print(out,verbose=TRUE)
    """ % (n_components, pen_brain, pen_behave))


# convert the results back to dataframes and then to numpy arrays
df_u = com.convert_robj(com.r('out[1]'))['u']
df_v = com.convert_robj(com.r('out[2]'))['v']

x_loadings = df_u.as_matrix()
y_loadings = df_v.as_matrix()

# #for future use; weighted timeseries
# np.save('brain_SCCAloading',x_loadings)
# np.save('behavior_SCCAloading',y_loadings)

#main output
idx = np.triu_indices(n_areas, 1)
corr_mat = np.zeros((n_areas, n_areas, n_components))

for i in range(n_components):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, i]
    corr_mat[..., i] = this_mat + this_mat.T


region_labels = np.load(expanduser(region_labels_fn))

fig = plt.figure(figsize=(50, 14))
fig.subplots_adjust(right=0.8)
vmim = corr_mat.max()
vmax = corr_mat.min()
for i in range(n_components):
    ax = fig.add_subplot(2, n_components, i + 1)
    brain = ax.matshow(corr_mat[..., i], vmin=corr_mat[...].min(), vmax=corr_mat[...].max(),
               cmap=plt.cm.RdBu_r)
    ax.set_xticks(np.arange(n_areas))
    ax.set_xticklabels(region_labels, rotation=90)
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(region_labels)
    cb_brain = fig.colorbar(brain)

    behav_ax = fig.add_subplot(2, n_components, i + n_components + 1)
    behav_arr = np.zeros((1, len(keys)))
    behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
    behav = behav_ax.matshow(behav_arr, vmin=y_loadings[:, i].min(), vmax=y_loadings[:, i].max(),
                     cmap=plt.cm.RdBu_r)
    behav_ax.set_xticks(np.arange(len(keys)))
    behav_ax.set_xticklabels(keys, rotation=90)
    cb_behave = fig.colorbar(behav, orientation='horizontal')

plt.savefig(result_corr_fn)
plt.close(fig)


# explained variable
import rcca
from sklearn.linear_model import LinearRegression

exp_var_X = []
exp_var_Y = []

if SCCA_exp_var_check==False:
	limit_exp_var = 30
	
for i in range(1, limit_exp_var+1):
    if SCCA_exp_var_check:

    	n_com = i
        com.r(
	        """
	        out <- CCA(x = X, z = Y, K = %i, niter = 100, standardize = FALSE,
	                   penaltyx = %f, penaltyz = %f)
	        print(out,verbose=TRUE)
	        """ % (n_com, pen_brain, pen_behave))
        # convert the results back to dataframes and then to numpy arrays
        df_u = com.convert_robj(com.r('out[1]'))['u']
        df_v = com.convert_robj(com.r('out[2]'))['v']
        x_loadings = df_u.as_matrix()
        y_loadings = df_v.as_matrix()

    else:
        # Set up Pyrcca
        cca = rcca.CCA(kernelcca=False, numCC=i, reg=1.)
        # Find canonical components
        cca.train([X, Y])

        x_loadings = cca.ws[0]
        y_loadings = cca.ws[1]

    P = x_loadings
    lr = LinearRegression(fit_intercept=False)
    lr.fit(P, X.T)
    rec_X = lr.coef_.dot(P.T)
    exp_var_X.append(1 - (np.var(X - rec_X) / np.var(X)))

    Q = y_loadings
    lr = LinearRegression(fit_intercept=False)
    lr.fit(Q, Y.T)
    rec_Y = lr.coef_.dot(Q.T)
    exp_var_Y.append(1 - np.var(Y - rec_Y) / np.var(Y))


plt.figure()
plt.plot(np.arange(limit_exp_var) + 1, exp_var_X, label='Brain exp var')
plt.plot(np.arange(limit_exp_var) + 1, exp_var_Y, label='Behavioral exp var')
plt.ylim(-0.1, 1)
plt.xlim(1, limit_exp_var)
plt.legend(loc='lower right')
plt.savefig('exp_var.pdf')
plt.close('all')