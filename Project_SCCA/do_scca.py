# keysfn = 'select_keys_MWQ_all.pkl'
# behavefn = 'select_data_MWQ_all.pkl'
keysfn = 'select_keys_MWQ.pkl'
behavefn = 'select_data_MWQ.pkl'

rscorrfn = 'cs_cross_corr_Bzdok_DMN18.npy'
corr_keys_fn = 'cs_cross_corr_Bzdok_DMN18_keys.npy'
region_labels_fn = 'cs_cross_corr_Bzdok_DMN18_ROIS.npy'

n_areas = 18

n_components = 5
pen_behave = 0.3
pen_brain = 0.1

result_corr_fn = 'MWQpca_BzdokDMN_penBehav%1.1f_penBrain%1.1f.pdf' %(pen_behave, pen_brain)
result_brain_fn = 'MWQpca_BzdokDMN_penBehav%1.1f_penBrain%1.1f_brain.pdf' %(pen_behave, pen_brain)


##############################################################################
from os.path import expanduser

from sklearn.cross_decomposition import CCA
from joblib import load
import numpy as np
import matplotlib.pyplot as plt


from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA


keys = load(expanduser(keysfn))
behavioral_data = load(expanduser(behavefn))

# # HACK
subjet_subset = behavioral_data[:, 0].astype('i4') - 1
keys = keys[5:]
behavioral_data = behavioral_data[:, 5:]

# keys = keys[1:]
# behavioral_data = behavioral_data[:, 1:]

rest_data = np.load(expanduser(rscorrfn))
#this is the number of selected regions
X = rest_data[subjet_subset]
Y = behavioral_data
S = Y.sum(axis=0) / Y.shape[0]
Y -= S[np.newaxis, :]
var = (Y ** 2).sum(axis=0)
var[var == 0] = 1
Y /= var

X[np.isnan(X)] = 1


import readline
import rpy2.rinterface as ri
import pandas.rpy.common as com
#panadas will not support this function in the future. 
#We need to find out how to use RPY2 to do the same thing
import pandas as pd

# load the Stanford package for SCCA
com.r("require(PMA)")

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

#for future use
np.save('brain_SCCAloading',x_loadings)
np.save('behavior_SCCAloading',y_loadings)

# fig = plt.figure(figsize=(30, 30))
# loading_range = np.arange(len(y_loadings))
# pace = 65
# for j, i in enumerate(range(0, len(y_loadings), pace)):
#     ax = fig.add_subplot(len(y_loadings) // pace + 1, 1, j + 1)
#     ax.plot(loading_range[i:(i + pace)], y_loadings[i:(i + pace)])
#     ax.plot(loading_range[i:(i + pace)],
#             np.zeros(len(loading_range[i:(i + pace)])), linestyle='--',
#             color='r')
#     ax.set_ylim([-0.3, 0.3])
#     ax.set_xlim(i, i + pace)
#     ax.set_xticks(loading_range[i:(i + pace)])
#     ax.set_xticklabels(keys[i:(i + pace)], rotation=90)
#     fig.tight_layout()
#     plt.savefig('cca.pdf')
# plt.close(fig)
# plt.close('all')


# #create region pairs for graph lable
corr_keys = np.load(expanduser(corr_keys_fn))
fig = plt.figure(figsize=(30, 30))
ax = fig.add_subplot(111)
ax.matshow(x_loadings)
ax.set_yticks(np.arange(len(corr_keys)))
ax.set_yticklabels(corr_keys)
plt.savefig(result_brain_fn)



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


# # In[800]:
import rcca
exp_var_X = []
exp_var_Y = []
for i in range(1, 31):
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
plt.plot(np.arange(30) + 1, exp_var_X, label='Brain exp var')
plt.plot(np.arange(30) + 1, exp_var_Y, label='Behavioral exp var')
plt.ylim(-0.1, 1)
plt.xlim(1, 30)
plt.legend(loc='lower right')
plt.savefig('exp_var.pdf')

plt.close('all')
