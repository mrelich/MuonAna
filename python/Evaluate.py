
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Evaluate the chosen model on the evaluation dataset and plot the #
# score from whatever model is used.                               #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

from MyData import Data

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt
from sklearn.externals import joblib

import numpy as np

#------------------------------------------------------#
# Method to evaluate and plot bdt score
#------------------------------------------------------#
def evaluate(dt_eval, dt_train, opts):
    
    # If modelinput is specified then read in model
    bdt = None
    if len(opts.modelinput) != 0:
        bdt = joblib.load(opts.modelinput)
        print "Loaded model back ", opts.bdtname
        print bdt        
    else:
        print "Model not specified..."
        print "Creating classification and training again"
        bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                                 algorithm = 'SAMME',
                                 n_estimators=opts.ntrees,
                                 learning_rate=opts.lrate)

        bdt.fit(dt_train.getDataNoWeight(), dt_train.targets)

    # Now get the bdt scores
    sig_scores = bdt.decision_function(dt_eval.getDataNoWeight()[dt_eval.targets > 0.5])
    bkg_scores = bdt.decision_function(dt_eval.getDataNoWeight()[dt_eval.targets < 0.5])

    # Get weights
    sig_weights = dt_eval.getDataWeights()[dt_eval.targets > 0.5]
    bkg_weights = dt_eval.getDataWeights()[dt_eval.targets < 0.5]


    # Print some information for a set of cuts
    cuts = np.arange(0,1,0.05)
    for cut in cuts:
        print "------------------------------------------"
        print "cut: ", cut
        print "\tSignal:    ", sum(sig_weights[ sig_scores > cut ])
        print "\tBackground:", sum(bkg_weights[ bkg_scores > cut ])

    # Make figure and axis
    fig, ax = plt.subplots(ncols=1, figsize=(10,7))

    # Set minimum and maximum for x-axis
    xminmax = (-1,1)

    # Make hist for signal
    plt.hist(sig_scores, weights=sig_weights,
             color='r',label='signal',range=xminmax,
             alpha=0.5,
             bins = 100, log=True,
             histtype='stepfilled')

    # Make hist for bkg
    plt.hist(bkg_scores, weights=bkg_weights,
             color='b',label='background',range=xminmax,
             alpha=0.5,
             bins = 100, log=True,
             histtype='stepfilled')
    
    # Miscellanous
    plt.xlabel("BDT output")
    plt.ylabel("Events / year / bin")
    plt.legend(loc='best')
    plt.grid()
    plt.xticks(np.arange(-1, 1.1, 0.1))
    #plt.xticks(np.arange(-5, 5.2, 0.5))
    #plt.semilogy()
    #ax.set_yscale("log")
    #plt.savefig("plots/evaluate/WeightedResult_"+opts.bdtname+".png")

    plt.show()

