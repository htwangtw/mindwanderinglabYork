import numpy as np
import warnings

def is_outliers(data, m=2.5):
	'''
	Just check outliers(boolean)
	'''
	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)
		mean = np.nanmean(data, axis=0)
		sd = np.sqrt(np.nanmean((data - mean)**2, axis=0))

	is_outliers = abs(data - mean) > m * sd
	return is_outliers

def imputedata(data, strategy='mean', missing=False):
	'''
	two impute strategys
	'''
	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)
		mean = np.nanmean(data, axis=0)
		sd = np.sqrt(np.nanmean((data - mean)**2, axis=0))
	sign = np.sign(data - mean)
	is_out = is_outliers(data, m=2.5)
	data[is_out] = np.nan
	
	if strategy == '2sd':
		# impute as +-2sd m
		# reduce the change in distribution. 
		for i in range(data.shape[1]):
			if missing:
				sign[np.isnan(sign)] = 0 #missing data will be imputed as mean
			ind_nan = np.where(np.isnan(data[:,i]))
			data[ind_nan,i] = mean[i] + (sd[i] * 2 * sign[ind_nan,i])

	if strategy == 'mean':
		#impute as mean
		for i in range(data.shape[1]):
			ind_nan = np.where(np.isnan(data[:,i]))
			if missing: #missing data will be imputed as mean
				data[ind_nan,i] = mean[i]
			else: #missing data will be left as nan
				data[ind_nan,i] = mean[i] * abs(sign[ind_nan,i])
	return data

def demean(Y):
	#it doesn't handle nan
	S = Y.sum(axis=0) / Y.shape[0]
	Y -= S[np.newaxis, :]
	var = (Y ** 2).sum(axis=0)
	var[var == 0] = 1
	Y /= var


def mean_nonzero(data, a):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        temp_sum = np.sum(data!=0, axis=a)
        temp_sum [temp_sum==0] = 1 
        output = np.sum(data, axis=a)/temp_sum
    return output

def quadratic1(a,b,c):
    if b**2-4*a*c < 0:
        x = np.nan
        print('No solution') 
    elif b**2-4*a*c==0: 
        x = -b/(2*a)
        print('Solution is',x) 
    else: 
        x = np.array(((-b+np.sqrt(b**2-4*a*c))/(2*a), (-b-np.sqrt(b**2-4*a*c))/(2*a)))
        print('Solutions are', x)
    return x