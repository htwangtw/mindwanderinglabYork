"""
Behavioral data preprocessing for CCA and other stuff (potentially)

Created on Wed 24 Feb 13:43:09 2016
Last updated on Thu 05th of May 2016

@author: Haoting

This script cleans the data of the cohort study or any other behavioral data in similar format.
It can
	1) select the variables you are interested in,  
	2) exclude cases with more than n missing cells among the selected variables,
	3) impute outlier with the mean or 2sd from mean of the variable.
	4) impute missing data with mean

Please ensure the following packages are installed if you are running on your personal machine:
	pandas, numpy, joblib, scikitlearn

You also need costumed module I make for general analysis. Please put it under your work directory.
	MWLAb_analysis.py

Put the script in the same directory of the raw behavior data. 

If you are using the preprocessed data for Sparse-CCA:
	-The id should match the subject id of the imaging data or the other set of behavioral data.
	-In other words, the same participant should have the same id across those two set of data.

"""
excludeNaN = False
WD = 'U:\\Projects\\Project_CCA'
behavData_xlsx = 'Behavioural\\mwq.raw_sessionMean.xlsx'

# Keywords in the selected variable, they have to match the exact name in the file               
# the first key you select must be the id
selectvar = False #if you dont need it, change to false
selectedKeys = ['SCAN_ID',
				'foo'
				]#don't touch if false

#optional: name the selected behavioral data; can leave unchanged; this will save data as .npy files
keysfn = 'keys_foo'
datafn = 'data_MWQ_session_preprocessed'
imp_s = 'mean' # impute strategy
drop_c = 10  #criteria of dropping participants: number of missing variable 
impute_miss = True #if you are using this output for SCCA, set as True. It will impute missing values with variable mean
#Run the script after changing the things above
##########################################################################DONT TOUCH##########################################################################
import pandas as pd
import numpy as np
import joblib
import os

os.chdir(WD)
#Load raw data
data_raw = pd.read_excel(behavData_xlsx)

#get all the keys of the raw data
keys= data_raw.columns
if selectvar:
	#select keys you are inculding in the analysis 
	includeKeys = []
	for s in selectedKeys:
	    for k in keys:
	        if s in k: 
	            includeKeys.append(k)
	# clean data
	# get the variable we are including
	cs_include = data_raw[includeKeys].values
	keys = includeKeys
else:
	cs_include = data_raw.values

excludeIdx = []
if excludeNaN:
	#exclde cases with more than 20 nan
	excludeIdx = []
	for i in range(cs_include.shape[0]):
	    n = np.count_nonzero(np.isnan(cs_include)[i])
	    if n>drop_c:
	        excludeIdx.append(i)

	excludeIdx = np.array(excludeIdx)
	#exclude the participants
	x = np.delete(cs_include, excludeIdx, 0)
	data = x[:,1:]
	IDNO = x[:,0]

else:
	data = cs_include[:,1:]
	IDNO = cs_include[:,0]


from MWLab_analysis import *
data_imp = imputedata(data, imp_s, missing=impute_miss) #impute outlier

#demean
S = data_imp.sum(axis=0) / data_imp.shape[0]
data_imp -= S[np.newaxis, :]
var = (data_imp ** 2).sum(axis=0)
var[var == 0] = 1
data_imp /= var

#save file
output = np.column_stack((IDNO, data_imp))

np.save(datafn, output)
# np.save(keysfn, keys)
# np.savetxt('foo.csv', output, fmt='%10.8f', delimiter=',')
