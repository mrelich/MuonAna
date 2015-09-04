
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Once the hyper-parameters and variables are chosen for the #
# machine learning method, run this script to test whether   #
# or not you are overtraining.  This will perform the k-fold #
# cross-validation.                                          #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

from MyData import Data
from Options import Options

from sklearn import cross_validation
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

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
                                              
