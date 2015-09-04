
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Initially I chose BDTs for this problem due to the fact they are   #
# easy to understand and widely used.  Let's see if we can find some #
# other methods that perform as good, or better!                     #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

from MyData import Data
import numpy as np
import Options as opts

from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

from sklearn.metrics import roc_curve, auc

import matplotlib.pyplot as plt

#-----------------------------------------------------#
# Function to run the classifiers
#-----------------------------------------------------#
def explore(dt_train, dt_test):

    # Old faithful
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                             algorithm = 'SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)
    

    # Bagging using k-nearest-neighbors
    knn = BaggingClassifier(KNeighborsClassifier())
    
    # Random Forest
    rforest = RandomForestClassifier(n_estimators=10)

    # Gradient boosting
    grb = GradientBoostingClassifier(n_estimators=opts.ntrees,
                                      learning_rate=opts.lrate,
                                      max_depth=3)

    
    # Put these guys into a list
    clfs = [(bdt,"BDT",'k'),
            (knn,"KNN",'r'),
            (rforest,"Random Forest",'g'),
            (grb, "Gradient Boosting",'b')
        ]

    # Now train them
    for clf in clfs:
        clf[0].fit(dt_train.getDataNoWeight(),
                   dt_train.targets)

    # Plotting stuff
    #fig, ax = plt.subplots(ncols=1, figsize=(7,6))
    for clf in clfs:
        print clf[1], clf[0].score(dt_test.getDataNoWeight(), dt_test.targets)
