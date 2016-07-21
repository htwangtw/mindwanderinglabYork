# import os
# os.chdir('U:\\Downloads')

import pandas as pd
df = pd.read_excel('PCA_TaskScores_new.xlsx',sheetname=0)
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
# %matplotlib inline
from scipy.cluster.hierarchy import dendrogram
# reorder rows with respect to the clustering
row_dendr = dendrogram(row_clusters, labels=labels, orientation='left')
df_rowclust = df.ix[row_dendr['leaves']]

# plot
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig = plt.figure(figsize=(df_rowclust.shape[0]*1.5,df_rowclust.shape[1]*5))
ax = fig.add_subplot(111)
im = ax.matshow(df_rowclust, vmin=-0.9, vmax=0.9, interpolation='nearest', cmap=plt.cm.RdBu_r)
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", "15%", pad="20%")
plt.colorbar(im, cax=cax)
ax.set_yticks(range(df_rowclust.shape[0]))
ax.set_xticks(range(df_rowclust.shape[1]))
ax.xaxis.set_ticks_position('top')
ax.set_xticklabels(list(df_rowclust.columns), fontsize='x-large', rotation=90)
ax.set_yticklabels(list(df_rowclust.index), fontsize='x-large')
plt.savefig('TaskScores_clustered.png')

# fig = plt.figure(figsize=(df.shape[0]*1.5,df.shape[1]*3))
# ax = fig.add_subplot(111)
# im = ax.matshow(df, vmin=-0.9, vmax=0.9, interpolation='nearest', cmap=plt.cm.RdBu_r)
# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("right", "15%", pad="20%")
# plt.colorbar(im, cax=cax)
# ax.set_yticks(range(df.shape[0]))
# ax.set_xticks(range(df.shape[1]))
# ax.xaxis.set_ticks_position('top')
# ax.set_xticklabels(list(df.columns), fontsize='medium', rotation=90)
# ax.set_yticklabels(list(df.index), fontsize='x-large')
# plt.savefig('COT.png')
# plt.close('all')


# fig = plt.figure(figsize=(df_rowclust.T.shape[0]*3,df_rowclust.T.shape[1]*3))
# ax = fig.add_subplot(111)
# im = ax.matshow(df_rowclust.T, vmin=-0.9, vmax=0.9, interpolation='nearest', cmap=plt.cm.RdBu_r)
# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("bottom", "15%", pad="20%")
# plt.colorbar(im, cax=cax, orientation='horizontal')
# ax.set_yticks(range(df_rowclust.shape[1]))
# ax.set_xticks(range(df_rowclust.shape[0]))
# ax.xaxis.set_ticks_position('top')
# ax.set_xticklabels(list(df_rowclust.index), fontsize='large', rotation=90)
# ax.set_yticklabels(list(df_rowclust.columns), fontsize='x-large')
# plt.savefig('PCA_hierarchical_aggolomerative_cluster_reversedEfficiencyScore.png')
# plt.show()

# fig = plt.figure(figsize=(df.T.shape[0]*1.5,df.T.shape[1]*3))
# ax = fig.add_subplot(111)
# im = ax.matshow(df.values.T, vmin=-0.9, vmax=0.9, interpolation='nearest', cmap=plt.cm.RdBu_r)
# divider = make_axes_locatable(plt.gca())
# cax = divider.append_axes("bottom", "15%", pad="20%")
# plt.colorbar(im, cax=cax, orientation='horizontal')
# ax.set_yticks(range(df.shape[1]))
# ax.set_xticks(range(df.shape[0]))
# ax.xaxis.set_ticks_position('top')
# ax.set_xticklabels(list(df.index), fontsize='large', rotation=90)
# ax.set_yticklabels(list(df.columns), fontsize='x-large')
# plt.savefig('foo.png')
# plt.show()