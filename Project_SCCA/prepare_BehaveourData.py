# -*- coding: utf-8 -*-
"""
Behavioral data preprocessing for CCA and other statistic learning methods

Created on Wed 24 Feb 13:43:09 2016
Last updated on Thu 11th of Mar 2016

@author: Haoting

This script cleans the data of the cohort study or any other behavioral data in similar format.
It can
	1) select the variables you are interested in,  
	2) exclude cases with more than 10 missing cells among the selected variables,
	3) replace the remaining missing cells with the mean of the variable.
2) and 3) are the strategies I selected. They are the most suitable for the cohort study and CCA(collected 2015/16)
If you want to use different criteria or missing data handling method, let me know. 
I intend to add a few selections in the future. 


Please ensure the following packages are installed if you are running on your personal machine:
	pandas, numpy, joblib, scikitlearn

Put the script in the same directory of the raw behavior data
Please check file 'CS_MergedDataset_12.02.16_N100.xlsx' as an example raw data file

If you are using the preprocessed data for Sparse-CCA:
	-The id should match the subject id of the imaging data or the other set of behavioral data.
	-In other words, the same participant should have the same id across those two set of data.

"""

behavData_xlsx = 'CS_SCCA_MINDW_SEM_BEHAV_TEXT_N138_05.04.16_correctID.xlsx'

#Keywords in the selected variable, they have to match the exact name in the file               
#the first key you select must be the id
selectedKeys = ['IDNO',
				'MWQ_'
				]

#optional: name the selected behavioral data; can leave unchanged
keysfn = 'select_keys_MWQ.pkl'	#must end with .plk
selectdatafn = 'select_data_MWQ.pkl'

#Run the script after changing the things above

##########################################################################DONT TOUCH##########################################################################
import pandas as pd
import numpy as np
import joblib

#Load raw data
data_raw = pd.read_excel(behavData_xlsx)
data_raw = data_raw.convert_objects(convert_numeric=True)

#get all the keys of the raw data
keys= data_raw.columns
#select keys you are inculding in the analysis 
includeKeys = []
for s in selectedKeys:
    for k in keys:
        if s in k: 
            includeKeys.append(k)

#save as pickle
prep_keys = np.array(includeKeys)
joblib.dump(prep_keys, keysfn)

#clean data
#get the variable we are including

cs_include = data_raw[includeKeys].values

#exclde cases with more than 10 nan
excludeIdx = []
for i in range(cs_include.shape[0]):
    n = np.count_nonzero(np.isnan(cs_include)[i])
    if n>10:
        excludeIdx.append(i)

excludeIdx = np.array(excludeIdx)

#exclude the participants
data = np.delete(cs_include, excludeIdx, 0)

#replace NaNs with means of the variables
from sklearn.preprocessing import Imputer

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)

data_impute = imp.fit_transform(data)
joblib.dump(data_impute, selectdatafn)

# #demean
# idno = data_impute[:,0]
# mean = data_impute[:,1:].mean(axis=0)
# demean = data_impute[:,1:] - mean[np.newaxis,:]
# data_dm= np.column_stack((idno,demean))
# #save data as pickles
# joblib.dump(data_dm, 'cs_select17_data_dm.pkl')



