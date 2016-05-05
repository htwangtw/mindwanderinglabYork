WD = '\\change\\to\\your\\workingdirectory'
behavData_xlsx = 'fuckoff.xlsx'
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
data_imp = imputedata(data, imp_s) 
output = np.column_stack((IDNO, data_imp))
np.savetxt('byeoutliers.csv', output, fmt='%10.8f', delimiter=',')
