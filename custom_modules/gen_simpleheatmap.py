import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def single_heatmaps(xls_data, sheetname, cMap, sizex, sizey, vmax, vmin, fontsize, heatmapfn):
    graphs = pd.read_excel(xls_data, sheetname=sheetname) #you can change to different sheet here
    data = graphs.values
    rows = list(graphs.index) #rows categories
    columns = list(graphs.columns) #column categories
    
    fig,ax=plt.subplots(figsize = (data.shape[0]*0.6,data.shape[1]*2.5)) #set plot size
    im = ax.matshow(data, interpolation='nearest', cmap=cMap, vmax=vmax, vmin=vmin) #generate a heatmap
    # im = ax.imhow(data, interpolation='nearest', cmap=cMap) #generate a heatmap with yaxis label at the bottom
    cb = fig.colorbar(im) #color bar generate
    # cb.ax.set_ylabel('''r''', rotation=270, labelpad=15, style='italic', fontsize=20) #set label of color bar

    ax.set_yticks(np.arange(data.shape[0]), minor=False) #set number of ticks
    ax.set_xticks(np.arange(data.shape[1]), minor=False)

    ax.set_xticklabels(columns, minor=False, fontsize=fontsize) #set label of ticks
    ax.set_yticklabels(rows, minor=False, fontsize=fontsize)

    # ax.set_xlabel('LOSO', fontsize=20) #set label of axis
    # ax.set_ylabel('BOOTS', fontsize=20)
    
    # fig.suptitle('''Consistency across sampling methods ''', fontsize=14, fontweight='bold') #set title of the heat map

    plt.savefig(heatmapfn)
    plt.close(fig)

single_heatmaps(xls_data='newheatmaps.xlsx', sheetname=0, cMap=plt.cm.RdBu_r, sizex=0.6, sizey=2.5, 
    vmax=0.9, vmin=-0.9, fontsize=18, heatmapfn='COT_2.png')

