
'''
This script examine the goodness of fit of the given penalty values.
It will tell you the percentage of explained data 
from one SCCA component to the maximum number you can have. 

the included behavioural data should include only the variables/tasks/participants
you are looking at in this analysis.
'''
n_components = 6
pen_brain = 0.3
pen_behave = 0.5
n_areas = 14

WD = 'U:\\PhDProjects\\Project_CCA'
behavefn = 'select_data_MWQ_sessionMean.npy' 
beh_keysfn = 'select_keys_MWQ.npy'
rscorrfn = 'cs_cross_corr_Bzdok_DMN14.npy'
exp_var_fn = 'BzdokDMN14_MWQ_exp_var_penBrain%1.1f_penBehav%1.1f.pdf' %(pen_brain, pen_behave)

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
import os
import pandas as pd
#set cd here

os.chdir(WD)


#load data
all_keys = np.load(expanduser(beh_keysfn))
all_behavioral_data = np.load(expanduser(behavefn))
subjet_subset = all_behavioral_data[:, 0].astype('i4') - 1
keys = all_keys[1:] #the first column is the scan id
behavioral_data = all_behavioral_data[:, 1:]

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

df_X = pd.DataFrame(X)
df_Y = pd.DataFrame(Y)
rmat_X = com.convert_to_r_matrix(df_X)
rmat_Y = com.convert_to_r_matrix(df_Y)

ri.globalenv['X'] = rmat_X
ri.globalenv['Y'] = rmat_Y

# explained variable
from sklearn.linear_model import LinearRegression
limit_exp_var = len(keys) #save for later
exp_var_X = []
exp_var_Y = []
for i in range(1, limit_exp_var+1):
	n_com = i
	com.r(
	    """
	    out <- CCA(x = X, z = Y, K = %i, niter = 100, standardize = FALSE,
	               penaltyx = %f, penaltyz = %f)
	    """ % (n_com, pen_brain, pen_behave))

	# convert the results back to dataframes and then to numpy arrays
	df_u = com.convert_robj(com.r('out[1]'))['u']
	df_v = com.convert_robj(com.r('out[2]'))['v']
	x_loadings = df_u.as_matrix()
	y_loadings = df_v.as_matrix()

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


plt.close('all')
plt.figure()
plt.plot(np.arange(limit_exp_var) + 1, exp_var_X, label='Brain exp var')
plt.plot(np.arange(limit_exp_var) + 1, exp_var_Y, label='Behavioral exp var')
plt.ylim(-0.1, 1)
plt.xlim(1, limit_exp_var)
plt.legend(loc='lower right')


np.set_printoptions(precision=3,suppress=True,linewidth=1000)
x = np.transpose(np.array([range(1, limit_exp_var+1)] +[exp_var_X]+[exp_var_Y]))

print ''
print 'Explained data proportion'
print '    n', '  exp_brain', '  exp_behaviour'
print x

plt.show()