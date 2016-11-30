MW_DIR = 'U:\Projects\CS_Analysis\CS_data'
SAVE_DIR = 'U:\Projects\CS_Analysis\CS_MWQ\CS_MWQ_txt'

import glob, os
mwq_raw = sorted(glob.glob(MW_DIR + os.sep + '\*easyhard*.csv'))

import pandas as pd
data_txt = []
data_id = []
data_date = []
missing = []
for tmp_raw_path in mwq_raw[0:10]:
	tmp_raw = pd.read_csv(tmp_raw_path)
	# if there's no lable 'inputMWC', mark as missing
	if 'inputMWC' in tmp_raw.keys():
		tmp_raw_txt = tmp_raw['inputMWC'].values[-1]
	# else append data
		if tmp_raw_txt:
			tmp_raw_id = tmp_raw['participant'].values[-1]
			tmp_raw_date = tmp_raw['date'].values[-1]

			data_txt.append(tmp_raw_txt)
			data_id.append(tmp_raw_id)
			data_date.append(tmp_raw_date)
		else:
			missing.append((tmp_raw_id,tmp_raw_date))


