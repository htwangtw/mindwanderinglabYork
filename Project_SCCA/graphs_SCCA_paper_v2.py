from os.path import expanduser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#reformat the loadings into the suitable format for the heat maps
keys = np.load(expanduser('sourcedata\\data_raw_keys_MWQ_master.npy'))[1:]
MWQ_keys = np.append(keys, keys)
MWQ_keys = np.append(MWQ_keys, keys)
loadings_lb = ['sourcedata\\SCCA_all_long.npy', 
	'sourcedata\\SCCA_LOSO_long.npy', 
	'sourcedata\\SCCA_bootstrap_long.npy']

y_loadings_1 = np.stack((-np.load(loadings_lb[0])[1][:,0], -np.load(loadings_lb[1])[1][:,0], -np.load(loadings_lb[2])[1][:,0]),axis=1)
y_loadings_2 = np.stack((np.load(loadings_lb[0])[1][:,1], -np.load(loadings_lb[1])[1][:,1], np.load(loadings_lb[2])[1][:,1]),axis=1)
y_loadings_3 = np.stack((np.load(loadings_lb[0])[1][:,3], np.load(loadings_lb[1])[1][:,2], -np.load(loadings_lb[2])[1][:,5]),axis=1)

y_loadings = np.vstack((y_loadings_1, y_loadings_2, y_loadings_3))


loadings_lb = ['sourcedata\\SCCA_all_brain_loading_mat.npy', 
	'sourcedata\\SCCA_LOSO_brain_loading_mat.npy', 
	'sourcedata\\SCCA_bootstrap_brain_loading_mat.npy']

x_loadings_1 = np.hstack((-np.load(loadings_lb[0])[...,0], -np.load(loadings_lb[1])[...,0], -np.load(loadings_lb[2])[...,0]))
x_loadings_2 = np.hstack((np.load(loadings_lb[0])[...,1], -np.load(loadings_lb[1])[...,1], np.load(loadings_lb[2])[...,1]))
x_loadings_3 = np.hstack((np.load(loadings_lb[0])[...,3], np.load(loadings_lb[1])[...,2], -np.load(loadings_lb[2])[...,5]))

x_loadings = np.vstack((x_loadings_1, x_loadings_2, x_loadings_3))

# basic info
n_components = 3
n_connects = 91
n_areas = 14

# slide 2: SCCA summary plots
RS_keys = ['1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4', '5', '6',
			'1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4', '5', '6',
			'1', '2', '3', '4', '1', '2', '3', '4', '1', '2', '3', '4', '5', '6',
			]
def RSC_plot(mat, ax):
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_xticks(np.arange(n_areas*3))
    ax.set_xticklabels(RS_keys, fontsize='large')
    ax.set_yticks(np.arange(n_areas*3))
    ax.set_yticklabels(RS_keys, fontsize='large')

    ax.plot([-0.5, 41.5], [-0.5, 41.5], ls='--', c='.3') 

    ax.plot([-0.5,27.5], [13.5,41.5], ls='--', c='.3')
    ax.plot([-0.5,13.5], [27.5,41.5], ls='--', c='.3')  
    ax.plot([13.5,41.5], [-0.5,27.5], ls='--', c='.3')
    ax.plot([27.5,41.5], [-0.5,13.5], ls='--', c='.3')


    ax.vlines(13.5, -0.5, 41.5) 
    ax.vlines(27.5, -0.5, 41.5) 

    ax.hlines(13.5, -0.5, 41.5) 
    ax.hlines(27.5, -0.5, 41.5) 

def MWQ_plot(mat, ax):
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_yticks(np.arange(len(MWQ_keys)))
    ax.set_yticklabels(MWQ_keys, fontsize='x-large')
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(['All', 'LOSO', 'BOOTS'], rotation=90)
    ax.vlines(1.5, -0.5, 38.5) 
    ax.vlines(0.5, -0.5, 38.5) 

    ax.hlines(12.5, -0.5, 2.5) 
    ax.hlines(25.5, -0.5, 2.5) 

    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", "50%", pad="30%")
    plt.colorbar(im, cax=cax)
    plt.tight_layout()

# create graphs
region_labels = np.load(expanduser('sourcedata\\data_cross_corr_Bzdok_DMN14_ROIS.npy'))
brain_mat = x_loadings
behav_arr = y_loadings
fig = plt.figure(figsize=(16,16))
fig.subplots_adjust(wspace = 0.5)
ax1 = plt.subplot2grid((4,4), (0, 0), colspan=3, rowspan=3)
ax2 = plt.subplot2grid((4,4), (0, 3), colspan=1, rowspan=3)
RS_plot(brain_mat, ax1)
MWQ_plot(behav_arr, ax2)
plt.tight_layout()
plt.savefig('SCCA_component.png')
plt.close(fig)

def heatmap(size, mat, x_keys, y_keys, filename): 
    fig,ax=plt.subplots(figsize=size) #set plot size
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)

    ax.set_yticks(np.arange(len(y_keys)))
    ax.set_yticklabels(y_keys, fontsize='x-large')
    ax.set_xticks(np.arange(len(x_keys)))
    ax.set_xticklabels(x_keys, rotation=90, fontsize='x-large')

    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", "20%", pad="20%")
    plt.colorbar(im, cax=cax)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)


def hierarchical_clustering(df):
	labels = list(df.index) #rows categories
	variables = list(df.columns) #column categories
	from scipy.spatial.distance import pdist,squareform
	row_dist = pd.DataFrame(squareform(pdist(df, metric='euclidean')), columns=labels, index=labels)

	from scipy.cluster.hierarchy import linkage
	row_clusters = linkage(pdist(df, metric='euclidean'), method='complete')
	pd.DataFrame(row_clusters, 
	             columns=['row label 1', 'row label 2', 'distance', 'no. of items in clust.'],
	             index=['cluster %d' %(i+1) for i in range(row_clusters.shape[0])])

	import matplotlib.pyplot as plt
	from scipy.cluster.hierarchy import dendrogram
	# reorder rows with respect to the clustering
	row_dendr = dendrogram(row_clusters, labels=labels, orientation='left')
	df_rowclust = df.ix[row_dendr['leaves']]
	return df_rowclust

# heat map: MWQ from SCCA
for i in range(3):
    behav_arr = np.zeros((len(keys),1))
    behav_arr.flat[:13] = y_loadings[0+ 13*i:13*(i+1),2]
    heatmap((3,3), behav_arr, ' ', keys,'SCCA_MWQ_comp_%i'%(i+1))

# heatmap: wellbeing
df = pd.read_excel('sourcedata\\PCA_questionnaires_wellbeing.xlsx', sheetname=1) #you can change to different sheet here
df_rowclust = hierarchical_clustering(df)
heatmap((10,6), df_rowclust, list(df_rowclust.columns), list(df_rowclust.index),'questionniare_2.png')

# heatmap: cognitive function
df = pd.read_excel('sourcedata\\PCA_TaskScores_new.xlsx', sheetname=0) #you can change to different sheet here
df_rowclust, labels, variables = hierarchical_clustering(df)
heatmap((10,8), df_rowclust, ['SEM','EXE','GEN'], row_dendr,'cognitivetasks.png')

