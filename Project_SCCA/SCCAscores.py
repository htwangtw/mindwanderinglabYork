os.chdir('U:\\PhDProjects\\Project_CCA\\Results')
behavedata = np.load(expanduser('data_MWQ_SCCADemean.npy'))
rest_data = np.load(expanduser('data_cross_corr_Bzdok_DMN14_SCCADemean.npy'))
y_loadings = np.load(expanduser('RSxMWQ_MWQ_SCCAloading.npy'))
x_loadings = np.load(expanduser('RSxMWQ_RS_SCCAloading.npy'))


comp = np.zeros((len(behavedata), y_loadings.shape[1]*2))
for i in range(y_loadings.shape[1]): 
	comp[:, i] = np.sum(rest_data*x_loadings[:,i],1)
	comp[:, i+6] = np.sum(behavedata*y_loadings[:,i],1)
comp = np.column_stack((subject_subset+1, comp))
np.savetxt('component_loadings_average.csv', comp, fmt='%10.8f', delimiter=',')