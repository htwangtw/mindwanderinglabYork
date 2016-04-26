# brain_loadings_s1 = x_loadings
# MWQ_loadings_s1 = y_loadings

# brain_loadings_s2 = x_loadings
# MWQ_loadings_s2 = y_loadings

# brain_loadings_s3 = x_loadings
# MWQ_loadings_s3 = y_loadings

# ###########################################################
brain_loadings_s1_clean = np.zeros((brain_loadings_s1.shape[0],3))
brain_loadings_s1_clean[:,0] = brain_loadings_s1[:,0]
brain_loadings_s1_clean[:,1] = brain_loadings_s1[:,1]
brain_loadings_s1_clean[:,2] = brain_loadings_s1[:,3]

MWQ_loadings_s1_clean = np.zeros((MWQ_loadings_s1.shape[0],3))
MWQ_loadings_s1_clean[:,0] = MWQ_loadings_s1[:,0]
MWQ_loadings_s1_clean[:,1] = MWQ_loadings_s1[:,1]
MWQ_loadings_s1_clean[:,2] = MWQ_loadings_s1[:,3]


x = np.abs(brain_loadings_s1_clean)*np.abs(brain_loadings_s2[:,0:3])*brain_loadings_s3[:,0:3]
y = np.abs(MWQ_loadings_s1_clean)*np.abs(MWQ_loadings_s2[:,0:3])*MWQ_loadings_s3[:,0:3]
x_loadings = np.sqrt(np.abs(x)) * np.sign(x)
y_loadings = np.sqrt(np.abs(y)) * np.sign(y)

# x_loadings = x
# y_loadings = y

idx = np.triu_indices(n_areas, 1)
corr_mat = np.zeros((n_areas, n_areas, 3))

for i in range(3):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, i]
    corr_mat[..., i] = this_mat + this_mat.T


region_labels = np.load(expanduser(region_labels_fn))

#test
fig = plt.figure(figsize=(20, 40))
fig.subplots_adjust(left=0.3, right=0.8, hspace = 0.4)
for i in range(3):
    ax = fig.add_subplot(3, 2, i*2 + 1)
    brain = ax.matshow(corr_mat[..., i], vmin=-1, vmax=1,
               cmap=plt.cm.RdBu_r)
    ax.set_xticks(np.arange(n_areas))
    ax.set_xticklabels(region_labels, rotation=90)
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(region_labels)
    # cb_brain = fig.colorbar(brain)

    behav_ax = fig.add_subplot(3, 2, (i + 1)*2)
    behav_arr = np.zeros((len(keys),1))
    behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
    # behav = behav_ax.matshow(behav_arr, vmin=y_loadings[:, i].min(), vmax=y_loadings[:, i].max(),
    #                  cmap=plt.cm.RdBu_r)
    behav = behav_ax.matshow(behav_arr, vmin=-1, vmax=1,
                     cmap=plt.cm.RdBu_r)
    behav_ax.set_yticks(np.arange(len(keys)))
    behav_ax.set_yticklabels(keys)
    cb_behave = fig.colorbar(behav)

plt.savefig('resultant_TOP3_test.pdf')
plt.close(fig)