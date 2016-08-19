n_components = 6
pen_brain = 0.3
pen_behave = 0.5
region_labels_fn = 'data_cross_corr_Bzdok_DMN14_preprocessed_ROIS.npy'
beh_keysfn = 'data_raw_keys_MWQ_master.npy'

WD = 'U:\\Projects\\Project_CCA'
'''
the included behavioural data should include only the variables/tasks/participants
you are looking at in this analysis.
The first column of your behavioural data must be participant number.

behavior participant number should be smaller than or equal to rs participant number.
ie. we have the RS data up to P145, the last participant you include should be P145 as well.
'''
behavefn = 'data_MWQ_session_preprocessed.npy'
rscorrfn = 'data_cross_corr_Bzdok_DMN14_preprocessed.npy'
loadingfn = 'RS_MWQ_SCCA_loadings_tuple.npy'

###################################################################################################
from os.path import expanduser
import numpy as np
from scca_r import SCCA_r
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
#set cd here
import os

def SCCA_Output_Sheet(filename, region_labels_fn, beh_keysfn, subject_subset, X, Y, loadings):
    x_loadings = loadings[0]
    y_loadings = loadings[1]

    n_components = x_loadings.shape[1]
    from MWLab_analysis import *
    n_connects = int(x_loadings.shape[0])
    temp_areas = quadratic1(1, -1, -2*n_connects)
    n_areas = int(temp_areas[temp_areas>0])

    idx = np.triu_indices(n_areas, 1)
    corr_mat = np.zeros((n_areas, n_areas, n_components))
    for i in range(n_components):
        this_mat = np.zeros((n_areas, n_areas))
        this_mat[idx] = x_loadings[:, i]
        corr_mat[..., i] = this_mat + this_mat.T
        
    np.save(filename + '_brain_loading_mat',corr_mat)

    region_labels = np.load(expanduser(region_labels_fn))
    keys = np.load(expanduser(beh_keysfn))[1:]
    fig = plt.figure(figsize=(20, 40))
    # fig = plt.figure()
    fig.subplots_adjust(left=0.3, right=0.8, hspace = 0.2, wspace = 0.4)
    for i in range(n_components):

        ax = fig.add_subplot(n_components, 2, i*2 + 1)

        brain = ax.matshow(corr_mat[..., i], vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
        ax.set_xticks(np.arange(n_areas))
        ax.set_xticklabels(region_labels, rotation=90)
        ax.set_yticks(np.arange(n_areas))
        ax.set_yticklabels(region_labels, fontsize='large')
        ax.plot([-0.5, 13.5], [-0.5, 13.5], ls='--', c='.3')
        # cb_brain = fig.colorbar(brain, fraction=0.046, pad=0.04)

        behav_ax = fig.add_subplot(n_components, 2, (i + 1)*2)
        behav_arr = np.zeros((len(keys),1))
        behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]
        behav = behav_ax.matshow(behav_arr, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
        behav_ax.set_yticks(np.arange(len(keys)))
        behav_ax.set_yticklabels(keys, fontsize='large')
        behav_ax.set_xticklabels(' ')
        cb_behave = fig.colorbar(behav, fraction=0.046, pad=0.04)
        # fig.tight_layout()

    plt.savefig(filename + '_heatmaps.pdf')
    plt.close(fig)

    comp = np.zeros((len(Y), y_loadings.shape[1]*2))
    for i in range(y_loadings.shape[1]): 
        comp[:, i] = np.sum(X*x_loadings[:,i],1)
        comp[:, i+n_components] = np.sum(Y*y_loadings[:,i],1)
    comp = np.column_stack((subject_subset+1, comp))
    headers = (',').join(['SIDNO']+['x_%i'%(i+1) for i in range(n_components)] + ['y_%i'%(i+1) for i in range(n_components)])
    with open(filename + '_component_loadings.csv', 'wb') as f:
        f.write(headers+'\n')
        np.savetxt(f, comp, fmt='%10.8f', delimiter=',')

from sklearn.linear_model import LinearRegression

def expVar(beh_keysfn, X,Y, penalty):
    keys = np.load(expanduser(beh_keysfn))[1:]
    limit_exp_var = len(keys) #save for later
    exp_var_X = []
    exp_var_Y = []
    for i in range(1, limit_exp_var+1):
        n_com = i
        loadings = SCCA_r(X,Y, n_com, penalty)

        x_loadings = loadings[0]
        y_loadings = loadings[1]
        
        '''
        calculate the coefficent of determination (R square): the proportion of 
        the proportion of the variance (fluctuation) of one variable that is predictable 
        from the other variable. In other words, the ratio of the explained variation to the total
        variation.
        '''
        
        P = x_loadings
        lr = LinearRegression(fit_intercept=False)
        lr.fit(P, X.T)
        rec_X = lr.coef_.dot(P.T)  #a.dot(b) equals np.dot(a,b)
        exp_var_X.append(1 - (np.var(X - rec_X) / np.var(X)))
        Q = y_loadings
        lr = LinearRegression(fit_intercept=False)
        lr.fit(Q, Y.T)
        rec_Y = lr.coef_.dot(Q.T)
        exp_var_Y.append(1 - np.var(Y - rec_Y) / np.var(Y))

    plt.close('all')
    plt.figure()
    plt.plot(np.arange(limit_exp_var) + 1, exp_var_X, label='Brain exp var')
    plt.plot(np.arange(limit_exp_var) + 1, exp_var_Y, label='Behavioral exp var')
    plt.ylim(-0.1, 1)
    plt.xlim(1, limit_exp_var)
    plt.legend(loc='lower right')

    np.set_printoptions(precision=3,suppress=True,linewidth=1000)
    x = np.transpose(np.array([range(1, limit_exp_var+1)] +[exp_var_X]+[exp_var_Y]))
    print ''
    print 'Explained data proportion'
    print '    n', '  exp_brain', '  exp_behaviour'
    print x
    plt.show()


############################################################################################
os.chdir(WD)

#load data
behavioral_data = np.load(expanduser(behavefn))
rest_data = np.load(expanduser(rscorrfn))
subject_subset = behavioral_data[:, 0].astype('i4') - 1

X = rest_data[subject_subset,:]
Y = behavioral_data[:,40:]

penalty = (pen_brain,pen_behave)
######################################################################################
expVar(beh_keysfn, X,Y, penalty)

loadings = SCCA_r(X, Y, n_components, penalty)
SCCA_Output_Sheet('Results\\SCCA_all_instances_new', region_labels_fn, beh_keysfn, subject_subset, X, Y, loadings)

np.save('SCCAloading_all_long',loadings)
np.save('X_SCCAraw',X)
# np.save('Y_SCCAraw',Y)

#################SCCA COMPLETE#################

Y_LOSO = np.load(expanduser('MWQ_data_trials_LOSO_set2.npy'))[:, 1:]
subject_subset = np.load(expanduser('MWQ_data_trials_LOSO_set2.npy'))[:, 0].astype('i4') - 1
X_LOSO = rest_data[subject_subset,:]

expVar(beh_keysfn, X_LOSO, Y_LOSO, penalty)

LOSO_loadings = SCCA_r(X_LOSO, Y_LOSO, n_components, penalty)
SCCA_Output_Sheet('SCCA_LOSO', region_labels_fn, beh_keysfn, subject_subset, X, Y, LOSO_loadings)
np.save('SCCAloading_LOSO_long',LOSO_loadings)

#################LOSO COMPLETE#################
import scikits.bootstrap as boot
data = (X, Y)
def SCCA_boot(X,Y):

    loadings = SCCA_r(X,Y, 6, (0.3,0.5))
    np.save('bootstrap_all_comp_long.npy', loadings)
    return True
ci_test = boot.ci(data, statfunction=SCCA_boot) 

boot_loadings = np.load(expanduser('bootstrap_all_comp_long.npy'))

# limit_exp_var = 13 #save for later
# exp_var_X = []
# exp_var_Y = []


SCCA_Output_Sheet('SCCA_Bootstrap_long', region_labels_fn, beh_keysfn, subject_subset, X, Y, boot_loadings)


from numpy import genfromtxt
data_by_task = genfromtxt('Behavioural\\mwq_byTask.csv', delimiter=',',skip_header=1)
data_CRT = data_by_task[:,1:14]
data_WM = data_by_task[:,14:]
subject_subset = data_by_task[:, 0].astype('i4')
loadings = boot_loadings[1]
comp = np.zeros((len(data_CRT), loadings.shape[1]*2))
for i in range(loadings.shape[1]): 
    comp[:, i] = np.sum(data_CRT*loadings[:,i],1)
    comp[:, i + loadings.shape[1]] = np.sum(data_WM*loadings[:,i],1)

comp = np.column_stack((subject_subset, comp))
headers = (',').join(['SIDNO']+['SCCA_Boots_CRT_%i'%(i+1) for i in range(n_components)] + ['SCCA_Boots_WM_%i'%(i+1) for i in range(n_components)])
with open('Results\\bootstrap_MWQbyTask_component_loadings.csv', 'wb') as f:
    f.write(headers+'\n')
    np.savetxt(f, comp, fmt='%10.8f', delimiter=',')


loadings = np.load(expanduser('SCCAloading_bootstrap.npy'))
loadings = loadings[1]
weighted_socre_CRT = np.zeros((loadings.shape[0],6))
weighted_socre_WM = np.zeros((loadings.shape[0],6))
for i in range(loadings.shape[1]): 
    weighted_socre_CRT[:, i] = np.mean(data_CRT*loadings[:,i],0)
    weighted_socre_WM [:, i] = np.mean(data_WM*loadings[:,i],0)

filename = 'SCCA_bootsrtap_bytask'

loadings = np.load(expanduser('SCCAloading_bootstrap.npy'))
x_loadings = loadings[0]
y_loadings = loadings[1]

n_components = x_loadings.shape[1]
from MWLab_analysis import *
n_connects = int(x_loadings.shape[0])
temp_areas = quadratic1(1, -1, -2*n_connects)
n_areas = int(temp_areas[temp_areas>0])

idx = np.triu_indices(n_areas, 1)
corr_mat = np.zeros((n_areas, n_areas, n_components))
for i in range(n_components):
    this_mat = np.zeros((n_areas, n_areas))
    this_mat[idx] = x_loadings[:, i]
    corr_mat[..., i] = this_mat + this_mat.T
    
np.save(filename + '_brain_loading_mat',corr_mat)

region_labels = np.load(expanduser(region_labels_fn))
keys = np.load(expanduser(beh_keysfn))[1:]
fig = plt.figure(figsize=(30, 40))
fig.subplots_adjust(left=0.3, right=0.8, hspace = 0.2, wspace = 0.4)
for i in range(n_components):

    ax = fig.add_subplot(n_components, 2, i*2 + 1)
    brain = ax.matshow(corr_mat[..., i], vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    ax.set_xticks(np.arange(n_areas))
    ax.set_xticklabels(region_labels, rotation=90)
    ax.set_yticks(np.arange(n_areas))
    ax.set_yticklabels(region_labels, fontsize='large')
    ax.plot([-0.5, 13.5], [-0.5, 13.5], ls='--', c='.3')
    # cb_brain = fig.colorbar(brain, fraction=0.046, pad=0.04)

    behav_ax = fig.add_subplot(n_components, 2, (i + 1)*2)
    behav_arr = np.zeros((len(keys),1))
    behav_arr.flat[:y_loadings.shape[0]] = y_loadings[:, i]

    heat_CRT_WM = np.zeros((loadings.shape[0], 3))
    heat_CRT_WM = np.column_stack((behav_arr, weighted_socre_CRT[:,i], weighted_socre_WM[:,i]))

    behav = behav_ax.matshow(heat_CRT_WM, vmin=-0.9, vmax=0.9, cmap=plt.cm.RdBu_r)
    behav_ax.set_yticks(np.arange(len(keys)))
    behav_ax.set_yticklabels(keys, fontsize='large')
    behav_ax.set_xticks(np.arange(3))
    behav_ax.set_xticklabels(['All', 'CRT','WM'], rotation=90)
    cb_behave = fig.colorbar(behav, fraction=0.046, pad=0.04)

plt.savefig(filename + '_heatmaps.pdf')
plt.close(fig)