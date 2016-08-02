
WD = 'U:\\Projects\\Project_CCA'
region_labels_fn = 'data_cross_corr_Bzdok_DMN14_ROIS.npy'
beh_keysfn = 'data_raw_keys_MWQ_master.npy'
result_corr_fn = 'Results\\SCCA_loadings_all.pdf'
SCCAloading_fn = 'RS_MWQ_SCCA_loadings_tuple.npy'
x_isconnectivity = True

import os
from os.path import expanduser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# os.chdir(WD)
# loadings = np.load(expanduser(SCCAloading_fn))
# x_loadings = loadings[0]
# y_loadings = loadings[1]

# keys = np.load(expanduser(beh_keysfn))[1:]
# n_components = x_loadings.shape[1]
# if n_components != y_loadings.shape[1]:
#     print('Wrong x and y loading pairs.')

# from MWLab_analysis import *
# #main output
# if x_isconnectivity:
#     n_connects = int(x_loadings.shape[0])
#     temp_areas = quadratic1(1, -1, -2*n_connects)
#     n_areas = int(temp_areas[temp_areas>0])

#     idx = np.triu_indices(n_areas, 1)
#     corr_mat = np.zeros((n_areas, n_areas, n_components))
#     for i in range(n_components):
#         this_mat = np.zeros((n_areas, n_areas))
#         this_mat[idx] = x_loadings[:, i]
#         corr_mat[..., i] = this_mat + this_mat.T

#     region_labels = np.load(expanduser(region_labels_fn))
#     fig = plt.figure(figsize=(20, 40))
#     # fig = plt.figure()
#     fig.subplots_adjust(left=0.3, right=0.8, hspace = 0.2, wspace = 0.4)
#     for i in range(n_components):

#         ax = fig.add_subplot(n_components, 2, i*2 + 1)

#         brain = ax.matshow(corr_mat[..., i], vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
#         ax.set_xticks(np.arange(n_areas))
#         ax.set_xticklabels(region_labels, rotation=90)
#         ax.set_yticks(np.arange(n_areas))
#         ax.set_yticklabels(region_labels, fontsize='large')
#         ax.plot([-0.5, 13.5], [-0.5, 13.5], ls='--', c='.3')
#         # cb_brain = fig.colorbar(brain, fraction=0.046, pad=0.04)

#         behav_ax = fig.add_subplot(n_components, 2, (i + 1)*2)
#         behav_arr = np.zeros((len(keys),1))
#         behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
#         behav = behav_ax.matshow(behav_arr, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
#         behav_ax.set_yticks(np.arange(len(keys)))
#         behav_ax.set_yticklabels(keys, fontsize='large')
#         behav_ax.set_xticklabels(' ')
#         cb_behave = fig.colorbar(behav, fraction=0.046, pad=0.04)
#         # fig.tight_layout()
    
#     plt.savefig(result_corr_fn)
#     plt.close(fig)

keys = np.load(expanduser('data_raw_keys_MWQ_master.npy'))[1:]
x_loadings = np.load('SCCAloading_LOSO.npy')[0]
y_loadings = np.load('SCCAloading_LOSO.npy')[1]
n_components = x_loadings.shape[1]
def RS_plot(mat, ax):
    im = ax.matshow(corr_mat[..., i], vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_xticks(np.arange(n_areas))
    ax.set_xticklabels(region_labels, rotation=90)
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(region_labels)
    ax.plot([-0.5, 13.5], [-0.5, 13.5], ls='--', c='.3')   

def MWQ_plot(mat, ax):
    im = ax.matshow(mat, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.locator_params(nbins=3)
    ax.set_yticks(np.arange(len(keys)))
    ax.set_xticklabels(' ')
    ax.set_yticklabels(keys, fontsize='large')
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", "50%", pad="30%")
    plt.colorbar(im, cax=cax)
    plt.tight_layout()


x_loadings[:,0:3] = -x_loadings[:,0:3]
y_loadings[:,0:3] = -y_loadings[:,0:3]
n_connects = int(x_loadings.shape[0])
temp_areas = quadratic1(1, -1, -2*n_connects)
n_areas = int(temp_areas[temp_areas>0])

idx = np.triu_indices(n_areas, 1)
corr_mat = np.zeros((n_areas, n_areas, n_components))
for i in range(n_components):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, i]
    corr_mat[..., i] = this_mat + this_mat.T

region_labels = np.load(expanduser('data_cross_corr_Bzdok_DMN14_ROIS.npy'))
for i in range(6):
    brain_mat = corr_mat[..., i]
    behav_arr = np.zeros((len(keys),1))
    behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
    fig = plt.figure()
    fig.subplots_adjust(wspace = 0.5)
    ax1 = plt.subplot2grid((1,4), (0, 0), colspan=3)
    ax2 = plt.subplot2grid((1,4), (0, 3), colspan=1)
    RS_plot(brain_mat, ax1)
    MWQ_plot(behav_arr, ax2)
    plt.tight_layout()
    # plt.show(fig)
    plt.savefig('SCCA_LOSO_component'+'_%i.png'%(i+1))
    plt.close(fig)
