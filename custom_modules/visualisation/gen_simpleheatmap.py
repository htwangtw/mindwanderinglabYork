import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def single_heatmaps(xls_data, sheetname, cMap, vmax, vmin, fontsize, heatmapfn):
    graphs = pd.read_excel(xls_data, sheetname=sheetname) #you can change to different sheet here
    data = graphs.values
    rows = list(graphs.index) #rows categories
    columns = list(graphs.columns) #column categories
    
    fig,ax=plt.subplots(figsize = (6,data.shape[1]+1)) #set plot size
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

    plt.savefig(heatmapfn,dpi=300)
    plt.close(fig)


#examples
single_heatmaps(xls_data='COT_heatmaps.xlsx', sheetname=0, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='COT_1.png')
single_heatmaps(xls_data='COT_heatmaps.xlsx', sheetname=1, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='COT_2.png')
single_heatmaps(xls_data='COT_heatmaps.xlsx', sheetname=2, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='COT_all.png')

single_heatmaps(xls_data='MS_in_Scanner.xlsx', sheetname=0, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='MS_taskprobes.png')
single_heatmaps(xls_data='MS_in_Scanner.xlsx', sheetname=1, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='MS_retro.png')

single_heatmaps(xls_data='PCA_forHeatmap_MWQ.xlsx', sheetname=0, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='CS_MWQ_trial.png')
single_heatmaps(xls_data='PCA_forHeatmap_MWQ.xlsx', sheetname=1, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='CS_MWQ_session.png')
single_heatmaps(xls_data='PCA_forHeatmap_MWQ.xlsx', sheetname=2, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='CS_MWQ_session_retro.png')
single_heatmaps(xls_data='PCA_forHeatmap_MWQ.xlsx', sheetname=3, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='CS_MWQ_RS.png')
single_heatmaps(xls_data='PCA_forHeatmap_MWQ.xlsx', sheetname=4, cMap=plt.cm.RdBu_r, vmax=0.9, vmin=-0.9, fontsize='x-large', heatmapfn='CS_MWQ_RS_retro.png')
