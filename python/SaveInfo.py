
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# On a larger scale for this analysis we need to save the bdt model   #
# to be run on data or other simulation.  In addition we should also  #
# save the split simulation into (I guess) root trees.                #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from MyData import Data
from Options import Options

from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.externals import joblib # recommended instead of pickle

from root_numpy import array2root
import numpy as np

#------------------------------------------------------#
# Train and pickle the model
#------------------------------------------------------#
def savemodel(dt_train, opts):
    
    # Make sure all model parameters are set in Options.py
    # TODO: Add Classifier options so we can use others 
    #       e.g. Gradient Boosting
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                             algorithm = 'SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)


    # Train the bdt
    bdt.fit(dt_train.getDataNoWeight(), dt_train.targets)

    # Write output to models
    joblib.dump(bdt, 'models/'+opts.bdtnamename+'.pkl')


#------------------------------------------------------#
# Save datasets to a root tree
#------------------------------------------------------#
def savedata(dt, basename, clf=None):
    
    # Get the data to write
    dt_out = dt.data
    labels = dt.t_varnames + ['w']

    # if a classifier is passed, then add that to the data field
    if clf != None:
        scores = clf.decision_function(dt.getDataNoWeight())
        dt_out = np.concatenate((dt_out, scores),axis=0)
        labels += ['score']

    # Move back to rec array
    reclabels = []
    row0 = dt_out[0]
    for i in range(len(row0)):
        reclabels.append((labels[i],row0[i].dtype))

    dt_out = np.array(dt_out, dtype=reclabels)
    print dt_out
    print dt_out['w'][0]


    # Separate the data into signal and background
    #dt_out_sig = dt_out[ dt.targets > 0.5 ]
    #dt_out_bkg = dt_out[ dt.targets < 0.5 ]

    #print dt_out_sig
    #print dt_out_sig.dtype
    #print dt_out_sig.dtype.names

    # Convert directly to a root file
    #array2root(dt_out_sig, basename + '_sig.root', 'tree')
    #array2root(dt_out_bkg, basename + '_bkg.root', 'tree')
    
    
