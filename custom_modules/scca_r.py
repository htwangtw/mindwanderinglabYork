import rpy2.rinterface as ri
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

pandas2ri.activate()
PMA = importr('PMA')

def SCCA_r(X,Y, n_components, pen):
	df_X = pd.DataFrame(X)
	df_Y = pd.DataFrame(Y)
	rmat_X = pandas2ri.py2ri(df_X)
	rmat_Y = pandas2ri.py2ri(df_Y)
	ri.globalenv['X'] = rmat_X
	ri.globalenv['Y'] = rmat_Y

	out = PMA.CCA(x=X, z=Y, K=n_components, niter =100, standardize=False, penaltyx=pen[0], penaltyz=pen[1])
	df_u = pandas2ri.ri2py(out[1])
	df_v = pandas2ri.ri2py(out[2])
	cors = pandas2ri.ri2py(out[15])
	
	loadings = (np.asmatrix(df_u), np.asmatrix(df_v))
	return loadings, cors