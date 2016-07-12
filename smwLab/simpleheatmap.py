import matplotlib.pyplot as plt

# WD = 'U:\\Projects\\Project_CCA\\Results\\LOSO' #where your raw data is 

raw_data = 'newheatmaps.xlsx' # your data for heatmap in a spreadsheet #only works with excel
output = 'COT_heeatmap1.png' #the name of your heatmap #keep as .png
colorMap = plt.cm.RdBu_r #don't change this 

####################################################################
# import os
# os.chdir(WD)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def single_heatmaps(xls_data,cMap, heatmapfn):
    graphs = pd.read_excel(xls_data,sheetname=0)
    data = graphs.values
    rows = list(graphs.index) #rows categories
    columns = list(graphs.columns) #column categories

    fig,ax=plt.subplots(figsize = (data.shape[0]*1.5,data.shape[1]*3))
    im = ax.matshow(data, interpolation='nearest', cmap=cMap)
    cb = fig.colorbar(im)

    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(columns, fontsize='x-large')
    ax.set_yticklabels(rows, fontsize='x-large')
    plt.savefig(heatmapfn)
    plt.close(fig)

single_heatmaps(xls_data=raw_data, cMap=colorMap, heatmapfn=output)