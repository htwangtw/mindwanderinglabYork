
from os.path import expanduser
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
        
    # np.save(filename + '_brain_loading_mat',corr_mat)

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

    # comp = np.zeros((len(Y), y_loadings.shape[1]*2))
    # for i in range(y_loadings.shape[1]): 
    #     comp[:, i] = np.sum(X*x_loadings[:,i],1)
    #     comp[:, i+n_components] = np.sum(Y*y_loadings[:,i],1)
    # comp = np.column_stack((subject_subset+1, comp))
    # headers = (',').join(['SIDNO']+['x_%i'%(i+1) for i in range(n_components)] + ['y_%i'%(i+1) for i in range(n_components)])
    # with open(filename + '_component_loadings.csv', 'wb') as f:
    #     f.write(headers+'\n')
    #     np.savetxt(f, comp, fmt='%10.8f', delimiter=',')

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