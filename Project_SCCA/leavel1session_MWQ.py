#load raw data
WD = 'U:\\Projects\\Project_CCA\\Behavioural'
behavData_xlsx = 'U:\\Projects\\CS_Analysis\\CS_MWQ\\MWQ_Lab.csv'
import warnings

import pandas as pd
import numpy as np
import os
from random import randint

# os.chdir(WD)
data_raw = pd.read_csv(behavData_xlsx,header=0)
SCAN_IDNO = np.unique(data_raw['SCAN_ID'])

keys = data_raw.columns
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


#generate participant - ignored session random list
for k in range(3):
	drop_sessions = np.array([randint(1,3) for p in range(165)])
	drop_sessions = np.column_stack((range(165), drop_sessions))
	#drop instance
	dropiloc = []
	for i in range(len(data_raw)):
		cur_s = data_raw.iloc[i,:]['session']
		cur_p = data_raw.iloc[i,:]['SCAN_ID']
		if cur_s == drop_sessions[cur_p,1]:
			dropiloc.append(i)

	data_selected = data_raw.drop(data_raw.index[dropiloc])
	data_selected = data_raw.drop(['session', 'date'],1)
	#separate trials and retrospective questions, mean by ID
	data_trials = data_selected.loc[data_selected['condition'] != 99].drop(keys[17:],1).drop('condition',1).groupby(['SCAN_ID']).mean().values
	# data_WM = data_selected.loc[data_selected['condition'] == 1].drop(keys[17:],1).drop('condition',1).groupby(['SCAN_ID']).mean().values
	# data_CRT = data_selected.loc[data_selected['condition'] == 2].drop(keys[17:],1).drop('condition',1).groupby(['SCAN_ID']).mean().values
	# data_sessions = data_selected.loc[data_selected['condition'] == 99].drop(['condition', 'MWQ_Focus'],1).groupby(['SCAN_ID']).mean().values
	#save to move on to prepare_behavior.py
	# from MWLab_analysis import *
	data_imp = imputedata(data_trials, '2sd', missing=True) #impute outlier
	S = data_imp.sum(axis=0) / data_imp.shape[0]
	data_imp -= S[np.newaxis, :]
	var = (data_imp ** 2).sum(axis=0)
	var[var == 0] = 1
	data_imp /= var
	# data_CRT_imp = imputedata(data_CRT, '2sd', missing=True) #impute outlier
	# data_WM_imp = imputedata(data_WM, '2sd', missing=True) #impute outlier
	# data_sessions_imp = imputedata(data_sessions, '2sd', missing=True) #impute outlier
	#save file

	output = np.column_stack((SCAN_IDNO, data_imp))
	np.save('MWQ_data_trials_LOSO_set%i'%k, output)

	# output = np.column_stack((SCAN_IDNO, data_CRT_imp))
	# np.save('MWQ_data_CRT_leave1out_set%i'%k, output)
	# output = np.column_stack((SCAN_IDNO, data_WM_imp))
	# np.save('MWQ_data_WM_leave1out_set%i'%k, output)
	# output = np.column_stack((SCAN_IDNO, data_sessions_imp))
	# np.save('MWQ_data_sessions_leave1out_set%i'%k, output)