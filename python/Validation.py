
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Once the hyper-parameters and variables are chosen for the #
# machine learning method, run this script to test whether   #
# or not you are overtraining.  This will perform the k-fold #
# cross-validation.                                          #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

from MyData import Data
from Options import Options
from TMVATest import test_train_compare

import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import time

#------------------------------------------------#
# Method to perform the k-fold validation
#------------------------------------------------#
def kvalidation(dt_dev, opts, k=3, njobs=2):

    # Create BDT
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                             algorithm='SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)

    # Perform validation
    scores = cross_validation.cross_val_score(bdt,
                                              dt_dev.getDataNoWeight(),
                                              dt_dev.targets,
                                              scoring="roc_auc",
                                              n_jobs=njobs,
                                              cv=k)

    # Print the result of the k-fold validation
    # TODO: Make this a plot or something...
    print "Validating BDT for following parameters:"
    print "\tnTrees =        ", opts.ntrees
    print "\tlearning rate = ", opts.lrate
    print "\tDepth         = ", opts.maxdepth
    print "Accuracy: %0.5f (+/- %0.5f)"%(scores.mean(), scores.std())

    print "----------------------------------------"
    print scores
    print
                                              

#------------------------------------------------#
# Method to perform the k-fold validation
#------------------------------------------------#
def k3validplot(dt_dev, opts):

    print "Running k3 validation plots"

    # Create BDT
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                             algorithm='SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)

    # Generate three equal datasets
    X1, X_temp, y1, y_temp = cross_validation.train_test_split(dt_dev.data,
                                                               dt_dev.targets,
                                                               train_size = 0.33,
                                                               random_state = 10293845)

    X2, X3, y2, y3 = cross_validation.train_test_split(X_temp, y_temp,
                                                       train_size = 0.5,
                                                       random_state = 56478392)

    # make data combinations
    def combine(d1,d2,t1,t2,name,sf):
        return Data(np.concatenate((d1,d2),axis=0),
                    np.concatenate((t1,t2),axis=0),
                    name,
                    sf)

    X12 = combine(X1,X2,y1,y2,"k1train",1)
    X13 = combine(X1,X3,y1,y3,"k2train",1)
    X23 = combine(X2,X3,y2,y3,"k3train",1)
    X1  = Data(X1, y1, "k1", 1)
    X2  = Data(X2, y2, "k2", 1)
    X3  = Data(X3, y3, "k3", 1)
    
    # Test on 3
    dt = time.time()
    print "k1 started...\t", time.time()    
    bdt.fit(X12.getDataNoWeight(), X12.targets)
    test_train_compare(bdt, X12, X3, "plots/validation/k1train_ztravelRemoved.png")

    # Test on 2
    print "k2 started...\t", time.time(), "time diff", time.time()-dt
    bdt.fit(X13.getDataNoWeight(), X13.targets)
    test_train_compare(bdt, X13, X2, "plots/validation/k2train_ztravelRemoved.png")

    # Test on 1
    print "k3 started...\t", time.time(), "time diff", time.time()-dt
    bdt.fit(X23.getDataNoWeight(), X23.targets)
    test_train_compare(bdt, X23, X1, "plots/validation/k3train_ztravelRemoved.png")

    print "End time: ", time.time(), "total run time: ", dt - time.time()
