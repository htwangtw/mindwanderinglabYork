from os.path import expanduser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#reformat the loadings into the suitable format for the heat maps
keys = np.load(expanduser('data_raw_keys_MWQ_master.npy'))[1:]
loadings_lb = ['SCCAloadings_all_long.npy', 'SCCAloading_LOSO.npy', 'SCCAloadings_bootstrap.npy']
x_loadings_1 = np.stack((-np.load(loadings_lb[0])[0][:,0], -np.load(loadings_lb[1])[0][:,0], -np.load(loadings_lb[2])[0][:,0]),axis=1)
x_loadings_2 = np.stack((-np.load(loadings_lb[0])[0][:,1], -np.load(loadings_lb[1])[0][:,1], np.load(loadings_lb[2])[0][:,1]),axis=1)
x_loadings_3 = np.stack((-np.load(loadings_lb[0])[0][:,3], np.load(loadings_lb[1])[0][:,2], -np.load(loadings_lb[2])[0][:,5]),axis=1)


y_loadings_1 = np.stack((-np.load(loadings_lb[0])[1][:,0], -np.load(loadings_lb[1])[1][:,0], -np.load(loadings_lb[2])[1][:,0]),axis=1)
y_loadings_2 = np.stack((-np.load(loadings_lb[0])[1][:,1], -np.load(loadings_lb[1])[1][:,1], np.load(loadings_lb[2])[1][:,1]),axis=1)
y_loadings_3 = -np.stack((np.load(loadings_lb[0])[1][:,3], np.load(loadings_lb[1])[1][:,2], -np.load(loadings_lb[2])[1][:,5]),axis=1)

y_loadings = np.vstack((y_loadings_1, y_loadings_2, y_loadings_3))
# y_loadings = np.stack((y_loadings_1, y_loadings_2, y_loadings_3), axis=2)
x_loadings = np.vstack((x_loadings_1, x_loadings_2, x_loadings_3))
# x_loadings = np.stack((x_loadings_1, x_loadings_2, x_loadings_3), axis=2)

n_components = 3
n_connects = 91
n_areas = 14


def RS_plot(mat, ax):
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_xticks(np.arange(n_areas*3))
    ax.set_xticklabels(range(15)[1:]*3, fontsize='large')
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(range(15)[1:], fontsize='large')
    ax.plot([-0.5, 13.5], [-0.5, 13.5], ls='--', c='.3') 
    ax.plot([13.5,27.5], [-0.5,13.5], ls='--', c='.3')
    ax.plot([27.5,41.5], [-0.5,13.5], ls='--', c='.3')  
    ax.vlines(13.5, -0.5, 13.5) 
    ax.vlines(27.5, -0.5, 13.5) 


def MWQ_plot(mat, ax):
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_yticks(np.arange(len(keys)))
    ax.set_yticklabels(keys, fontsize='x-large')
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(['All', 'LOSO', 'BS'], rotation=90)
    ax.vlines(1.5, -0.5, 12.5) 
    ax.vlines(0.5, -0.5, 12.5) 
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", "50%", pad="30%")
    plt.colorbar(im, cax=cax)
    plt.tight_layout()

n_ana = 3
idx = np.triu_indices(n_areas, 1)
x_loadings_mat = np.zeros((n_areas, n_areas*n_ana, n_components))
for i in range(n_ana):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, 0, i]
    this_mat_wide = this_mat + this_mat.T
    this_mat[idx] = x_loadings[:, 1, i]
    this_mat_wide = np.hstack((this_mat_wide,(this_mat + this_mat.T)))
    this_mat[idx] = x_loadings[:, 2, i]
    x_loadings_mat[..., i] = np.hstack((this_mat_wide,(this_mat + this_mat.T)))

region_labels = np.load(expanduser('data_cross_corr_Bzdok_DMN14_ROIS.npy'))

for i in range(3):
	brain_mat = x_loadings_mat[..., i]
	behav_arr = np.zeros((len(keys),3))
	behav_arr.flat[:39] = y_loadings[..., i]
	fig = plt.figure(figsize=(16,4))
	fig.subplots_adjust(wspace = 0.5)
	ax1 = plt.subplot2grid((1,4), (0, 0), colspan=3)
	ax2 = plt.subplot2grid((1,4), (0, 3), colspan=1)
	RS_plot(brain_mat, ax1)
	MWQ_plot(behav_arr, ax2)
	plt.tight_layout()
	plt.savefig('SCCA_component'+'_%i.png'%(i+1))
	plt.close(fig)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

graphs = pd.read_excel('LOSO_BOOTS_CORR.xlsx',sheetname=0)
def single_heatmaps(graphs,cMap, heatmapfn):
    data = graphs.values
    rows = list(graphs.index) #rows categories
    columns = list(graphs.columns) #column categories

    fig,ax=plt.subplots(figsize = (data.shape[0]*3,data.shape[1]*2))
    im = ax.imshow(data, interpolation='nearest', cmap=cMap, vmin=-0.4, vmax=1)

    cb = plt.colorbar(im)
    cb.set_label('Pearson\'s R', size=20)

    # plt.title('Correlation of Resutls', size=20)
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(columns, size=20)
    ax.set_yticklabels(rows, size=20)
    ax.set_xlabel('LOSO', size=24)
    ax.set_ylabel('Bootstrapping', size=24)
    plt.show()

    plt.savefig(heatmapfn)
    plt.close(fig)

single_heatmaps(graphs,plt.cm.Greens, 'corr.png')