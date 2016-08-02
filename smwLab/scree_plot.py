from numpy import genfromtxt
eigen = genfromtxt('PCA_eigen.csv', delimiter=',')[1:,:]

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,5))
sing_vals = np.arange(21) + 1
plt.plot(sing_vals, eigen[:,0].T, 'ro-', linewidth=2)
plt.plot([3.5,3.5], [0,6], ls='--', c='.4', linewidth=2)  
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Eigenvalue')
#I don't like the default legend so I typically make mine like below, e.g.
#with smaller fonts and a bit transparent so I do not cover up data, and make
#it moveable by the viewer in case upper-right is a bad place for it 
leg = plt.legend(['Eigenvalues from Task Score'], loc='best', borderpad=0.3, 
                 shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
                 markerscale=0.4)
leg.get_frame().set_alpha(0.4)
leg.draggable(state=True)
plt.show()


# make a square figure and axes
plt.figure(1, figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
labels = 'Semantics', 'Executive', 'Generativity', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
fracs = eigen[:,1]
explode=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
cmap = plt.cm.gray_r
colors = cmap(np.linspace(0., 1., len(fracs)))


# The slices will be ordered and plotted counter-clockwise.
plt.pie(fracs, explode=explode, 
	# labels=labels, 
	colors=colors,
	shadow=False, 
	startangle=200,
	# autopct='%1.1f%%'
	)

plt.show()

