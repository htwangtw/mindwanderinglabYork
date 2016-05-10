import numpy as np
import pandas as pd
from os.path import expanduser


MWQ_RAW = pd.read_excel('C:\\Users\\hw1012\\Documents\\Project_CCA\\mwq.raw_sessionMean.xlsx')
MWQ_RAW = MWQ_RAW[MWQ_RAW['condition']<99].sort(['SCAN_ID'])
MWQ_TRIAL = MWQ_RAW.drop(MWQ_RAW.columns[18:],1)

data = MWQ_RAW.values[:, 40:53]
data_CRT = MWQ_TRIAL[MWQ_TRIAL['condition']==1].values[:,5:]
data_WM = MWQ_TRIAL[MWQ_TRIAL['condition']==2].values[:,5:]

#avergae question scores by participants

behave_loading = np.load(expanduser('C:\\Users\\hw1012\\Documents\\Project_CCA\\behavior_SCCAloading.npy'))
brain_loading = np.load(expanduser('C:\\Users\\hw1012\\Documents\\Project_CCA\\brain_SCCAloading.npy'))
weights = [behave_loading, brain_loading]

loadings = np.zeros((len(data_CRT), behave_loading.shape[1]*4))

data = [data_CRT, data_WM]
#
for i in range(behave_loading.shape[1]): 
	loadings[:, i] = np.sum(data_CRT * brain_loading[:,i],1)
	loadings[:, i+6] = np.sum(data_CRT * behave_loading[:,i],1)
	loadings[:, i+12] = np.sum(data_WM * brain_loading[:,i],1)
	loadings[:, i+18] = np.sum(data_WM * behave_loading[:,i],1)
	
x = np.column_stack((subject_subset+1, loading))

np.savetxt('foo.csv', x, fmt='%10.8f', delimiter=',')