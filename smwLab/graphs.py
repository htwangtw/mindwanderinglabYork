import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def single_heatmaps(xls_data,cMap, heatmapfn):
    graphs = pd.read_excel(xls_data,sheetname=0)
    data = graphs.values
    rows = list(graphs.index) #rows categories
    columns = list(graphs.columns) #column categories

    fig,ax=plt.subplots(figsize = (data.shape[0]*1.5,data.shape[1]*1.5))
    im = ax.matshow(data, interpolation='nearest', cmap=cMap)
    cb = fig.colorbar(im)

    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(columns, rotation=90)
    ax.set_yticklabels(rows)
    plt.savefig(heatmapfn)
    plt.close(fig)

