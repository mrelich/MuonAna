
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

from root_numpy import array2root, array2tree
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
    #joblib.dump(bdt, 'models/'+opts.bdtname+'.pkl')
    joblib.dump(bdt, 'models/'+opts.bdtname+'_moretrainingdata_wllh.pkl')


#------------------------------------------------------#
# Save datasets to a root tree
#------------------------------------------------------#
def savedata(dt, basename, clf=None):
    
    # Get the data to write
    dt_out = dt.data
    labels = dt.treenames + dt.w_varnames + ['w']

    # if a classifier is passed, then add that to the data field
    if clf != None:
        scores = clf.decision_function(dt.getDataNoWeight())
        scores = scores.reshape((len(scores),1))
        dt_out = np.concatenate((dt_out, scores),axis=1)
        labels += ['score']


    csl = ""
    for i in range(len(labels)-1):
        csl += labels[i] + ","
    csl += labels[-1]
    print csl

    # Separate the data into signal and background
    dt_out_sig = dt_out[ dt.targets > 0.5 ]
    dt_out_bkg = dt_out[ dt.targets < 0.5 ]

    # Turn into record array
    dt_out_sig = np.rec.fromrecords(dt_out_sig, names=csl)
    dt_out_bkg = np.rec.fromrecords(dt_out_bkg, names=csl)

    # Convert directly to a root file
    array2root(dt_out_sig, basename + '_sig.root', 'tree','recreate')
    array2root(dt_out_bkg, basename + '_bkg.root', 'tree','recreate')
    
