
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# I am not sure about with a bdt, but some cuts are not necessary and     #
# don't contribute well to the overall score.  This script aims to see    #
# which cut is helping or hurting by training the bdt using n-1 datasets. #
# The default 'best' hyper parameters are chosen.                         #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from Options import Options
from MyData import Data

import pandas as pd
import numpy as np

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

#-------------------------------------------------------------------#
# Method to run the n-1 check
#-------------------------------------------------------------------#
def n1check(d_train, d_test, opts):

    # Load the data with no weights and put it into panda format
    # for easier manipulation
    pd_train = pd.DataFrame(d_train.getDataNoWeight())
    pd_test  = pd.DataFrame(d_test.getDataNoWeight())

    # Holder for results
    results = {}

    # Setup classifier
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                             n_estimators = opts.ntrees,
                             learning_rate = opts.lrate)

    # Train the classifier on total data set for comparison
    clf.fit(pd_train, d_train.targets)
    results['total'] = roc_auc_score(d_test.targets, clf.decision_function(pd_test))


    # Loop over the variables and store the results in dict
    keys    = d_train.t_varnames
    for i in range(len(keys)):
        
        sub_train = pd_train.drop(i,axis=1)
        sub_test  = pd_test.drop(i,axis=1)

        clf.fit(sub_train, d_train.targets)
        results[keys[i]] = roc_auc_score(d_test.targets, clf.decision_function(sub_test))


    # Now that we have the results, print all information
    print "--------------------------------------------"
    for key in results:
        print "Leaving out ", key, "gives score: ", results[key]
    print ""
