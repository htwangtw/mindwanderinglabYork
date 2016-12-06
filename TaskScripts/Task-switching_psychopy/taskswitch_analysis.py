'''
Before running this file, please check:
1) all the participant and session information on the FILENAMES are correct.
2) all the participant and session information in the file are stroed under correct columns.
3) logs with wrong data are not in the data directory if you want to run in batch
4) this file can handle single data log
'''

# raw data directory
# i.e. DATA_DIR = 'R:\LabData\CohortData\TaskSwitch\*_taskswitching*.csv'
DATA_DIR = 'R:\\Cohort_2016-2017\\Session2\\Task-switching_Psychopy\\taskswitching_data\\5*_taskswitching*.csv'

# results 
# i.e. RESULT_DIR = 'U:\Projects\CS_Analysis\Results'
RESULT_DIR = 'U:\\Projects\\CS3_Analysis\\Results'

# task name. use in the result output file
EXPNAME = 'TaskSwitch'

# Are you only analysing a sub set?
subset = True

# A list of participant number
# This must match the IDs on the csv filename
PPT_ID = [500
			]


################################################ Advanced settings. ####################################################################
'''
These variables have already been set for the analysis. No cofiguration required. 
'''

# the list of lable name(s) for independent varable(s) you care in your files
# i.e. multiple variables: Label_IV = ['dimension', 'CSI', 'type']
# i.e. only one variables: Label_IV = ['dimension']
Label_IV = ['dimension', 'CSI', 'type'] 

# the list of lable name(s) for dependent varable(s) you care in your files
# i.e. multiple variables: Label_DV = ['resp.rt', 'resp.corr']
# i.e. only one variables: Label_DV = ['resp.rt']
Label_DV = ['resp.rt', 'resp.corr']

# the lable name for indexing the data, such as participant id or session number in a file
# i.e. Lable_id = ['participant']
# if there are more than one variable, please keep participant number as the first one
Lable_idx = ['participant']

################################################ Do not change things below this line. ################################################ 
################################################ Load ExpAnalysis.py ################################################ 

import pandas as pd 
import numpy as np 
import glob, os, sys, errno
import itertools

def get_DIRs(DATA_DIR, subset, PPT_ID):
	'''
	DATA_DIR: string; 
	raw data directory with filename patten; 
	i.e. DATA_DIR = 'R:\LabData\CohortData\TaskSwitch\*_taskswitching*.csv'

	subset: True or False; 
	True if you are only analysing some participants

	PPT_ID: list
	A list of participant number; This must match the IDs on the csv filename

	'''
	DATA_DIR = sorted(glob.glob(DATA_DIR))
	if subset:
		check_id = []
		for d in DATA_DIR:
			check_id.append(int(d.split(os.sep)[-1].split('_')[0]))
		check_id = sorted(check_id)

		if set(PPT_ID).issubset(check_id)==False:
			sys.exit('The participant ID list and the log files doesn\'t match. Please check your data under %s and variable PPT_ID.' %DATA_DIR)

		DIRs = []
		for d in DATA_DIR:
			cur_id = int(d.split(os.sep)[-1].split('_')[0])
			if cur_id in PPT_ID:
				DIRs.append(d)

	else:
		DIRs = DATA_DIR

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
		if len(Lable_idx) > 0:
			df_cur_dat[Lable_idx[0]] = list(itertools.repeat(cur_id, df_cur_dat.shape[0]))
		else:
			df_cur_dat['IDNO'] = list(itertools.repeat(cur_id, df_cur_dat.shape[0]))

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
	df.to_csv(RESULT_DIR + os.sep + EXPNAME + '_' + FILENAME + '.csv', index=True)

#####################################################CONCATENATE FILES#######################################################
DIRs = get_DIRs(DATA_DIR, subset, PPT_ID)
df_long = concat_data_csvs(DIRs, Lable_idx, Label_IV, Label_DV)

# concatenate all the dataframes into long form and drop the first two cases
df_long = df_long.dropna(subset=['type'])

# deleate all the practice trials
practice_query = 'CSI != 0.5'
df_long = df_long.query(practice_query)

# # debug: dump to disc
# save_csv(df_long, RESULT_DIR, EXPNAME, FILENAME='long')
#####################################################RUN ANALYSIS#######################################################

# summary wide data: mean RT and ACC of each condition 
df_summary = dict()
for IV in Label_IV:
	df_IV = pd.pivot_table(df_long, values=Label_DV, index=['participant'],
		columns=IV, aggfunc=np.mean)
	df_summary[IV] = df_IV

df_wide = pd.concat(df_summary, axis=1)

#rename all the multi level headers to single level headers
new_col = []
for col in df_wide.columns.values:
	dv_type = col[1].split('.')[1]
	if dv_type == 'corr':
		dv_type = 'acc'

	try:
		cur_var = '_'.join([col[2], dv_type.upper()])
	except TypeError:
		cur_var = '_'.join([col[0], str(col[2]), dv_type.upper()])
	new_col.append(cur_var)

df_wide.columns = new_col


#Task switch special:
# THE LABEL NAMES IN COHORT 1 AND 3 ARE DIFFERENT, PLEASE CHECK and select the appropriate ones

# # CS1
# # contrast: switch cost = (control rt +uncategroised switch rt)/2 - repeat rt; smaller = good
# df_wide['SWITCHCOST'] = (df_wide['con_RT'] +df_wide['un_RT'])/2 - df_wide['re_RT']
# # contrast: inhibition = inhibitory - control; higher = good
# df_wide['INHIBITION'] =  df_wide['inhib_RT']- df_wide['con_RT']

# CS3
# contrast: switch cost = (control rt +uncategroised switch rt)/2 - repeat rt; smaller = good
df_wide['SWITCHCOST'] = (df_wide['CON_RT'] +df_wide['UCS_RT'])/2 - df_wide['REP_RT']
# contrast: inhibition = inhibitory - control; higher = good
df_wide['INHIBITION'] =  df_wide['INH_RT']- df_wide['CON_RT']

# dump to disk

if len(DIRs)==1: # single data file
	ppt = (df_long.participant.values[0])
	FILENAME = 'summary_' + str(ppt)
	save_csv(df_wide, RESULT_DIR, EXPNAME, FILENAME)
else: # batch analysis
	FILENAME = 'summary' 
	save_csv(df_wide, RESULT_DIR, EXPNAME, FILENAME)
