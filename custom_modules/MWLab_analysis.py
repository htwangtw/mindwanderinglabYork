import numpy as np
import warnings, errno
import pandas as pd 
import glob, os, sys
import itertools

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
	two impute strategys: '2sd' and 'mean'
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
	return Y /= var



def mean_nonzero(data, a):
	'''
	get means of all the non zero items along axis a
	'''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        temp_sum = np.sum(data!=0, axis=a)
        temp_sum [temp_sum==0] = 1 
        output = np.sum(data, axis=a)/temp_sum
    return output

def quadratic1(a,b,c):
	'''
	as function name
	'''
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

def get_DIRs(DATA_PATH, subset=False, PPT_ID=[]):
	'''
	DATA_PATH: string; 
	raw data directory with filename patten; 
	i.e. DATA_DIR = 'R:\LabData\CohortData\TaskSwitch\*_taskswitching*.csv'

	subset: True or False; 
	True if you are only analysing some participants

	PPT_ID: list
	A list of participant number; This must match the IDs on the csv filename

	'''
	DATA_PATH = sorted(glob.glob(DATA_DIR))
	if subset:
		check_id = []
		for d in DATA_PATH:
			check_id.append(int(d.split(os.sep)[-1].split('_')[0]))
		check_id = sorted(check_id)

		if set(PPT_ID).issubset(check_id)==False:
			sys.exit('The participant ID list and the log files doesn\'t match. Please check your data under %s and variable PPT_ID.' %DATA_DIR)

		DIRs = []
		for d in DATA_PATH:
			cur_id = int(d.split(os.sep)[-1].split('_')[0])
			if cur_id in PPT_ID:
				DIRs.append(d)

	else:
		DIRs = DATA_PATH

	return DIRs


def concat_data_csvs(DIRs, Lable_idx, Label_IV, Label_DV):
	'''
	The IDs on the csv filename must be correct.
	The filename should be: [PPT_ID]_[SESSION]_[otherStuff].csv

	DIRs: list;
	a list of file paths

	Lable_idx: list
	the lable name for indexing the data, such as participant id or session number in a file
	i.e. Lable_id=['participant']
	if there are more than one variable, please keep participant number as the first one	
	the list of lable name(s) for independent varable(s) you care in your files

	Label_IV: list
	i.e. multiple variables: Label_IV=['dimension', 'CSI', 'type']
	i.e. only one variables: Label_IV=['dimension']
	
	Label_DV: list
	the list of lable name(s) for dependent varable(s) you care in your files
	i.e. multiple variables: Label_DV=['resp.rt', 'resp.corr']
	i.e. only one variables: Label_DV=['resp.rt']

	'''
	def label_check(DIRs, Label_var):
		'''
		Check the labels are correctly spelt.
		This is just a sanity check on the first file.
		'''
		#load a dummy file to check the informations
		tmp_dat = pd.read_csv(DIRs[0], sep=',', header=0)
		tmp_keys = tmp_dat.keys().values.tolist()
		if set(Label_var).issubset(tmp_keys):
			pass
		else:
			sys.exit('Some label(s) do not exist in file %s. Are you sure all the variables are correctly spelt?' %DIRs[0])

	Label_var = Label_IV + Label_DV + Lable_idx

	label_check(DIRs, Label_var)
	# create a empty entry for storing data frames
	df_collect = dict()
	for p in DIRs:

		# get rt, acc, condition information
		df_cur = pd.read_csv(p, sep=',', header=0)
		if set(Label_var).issubset(df_cur.keys().values.tolist()):
			df_cur_dat = df_cur[Label_var]
		else: 
			for v in Label_var:
				if set(v).issubset(df_cur.keys().values.tolist()):
					pass
				else:
					df_cur_dat[v] = None # create empty varaible for missing variables

		# get id
		# use the id on the file name as the acutal id
		cur_id = int(p.split(os.sep)[-1].split('_')[0])
		df_cur_dat[Lable_idx[0]] = list(itertools.repeat(cur_id, df_cur_dat.shape[0]))

		# save the participant's data to a dictionary
		df_collect[p.split(os.sep)[-1]] = df_cur_dat
		
		return pd.concat(df_collect, axis=0) # concatenate all the dataframes into long form

def save_csv(df, RESULT_DIR, EXPNAME, FILENAME): 
	'''
	save a panda dataframe as a csv file
	'''
	# check if there's a result directory
	try:
	    os.makedirs(RESULT_DIR)
	except OSError as exception:
	    if exception.errno != errno.EEXIST:
	        raise    
	#dump to disc
	df.to_csv(RESULT_DIR + os.sep + EXPNAME + '_' + FILENAME + '.csv', index=False)