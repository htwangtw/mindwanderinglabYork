'''
impute data

Last updated on Thu 05th of May 2016
@author: Haoting


The data should have labels and the fiest column is participant number.
If not, modify yourself. The script is very straight forward.

You also need costumed module I make for general analysis. Please put it under your work directory.
	MWLAb_analysis.py

'''
WD = 'U:\\PhDProjects\\Project_CCA'
behavData_xlsx = 'Results\\component_loadings_leaveoneout.xlsx'
imp_s = '2sd' #selections: mean or 2sd
import pandas as pd
import numpy as np
import os
os.chdir(WD)
data_raw = pd.read_excel(behavData_xlsx)
keys= data_raw.columns
data = data_raw.values[:,1:]
IDNO = data_raw.values[:,0]
from MWLab_analysis import *
data_imp = imputedata(data, imp_s, missing=False) 
output = np.column_stack((IDNO, data_imp))
np.savetxt('impute_0606.csv', output, fmt='%10.8f', delimiter=',')