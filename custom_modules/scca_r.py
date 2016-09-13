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