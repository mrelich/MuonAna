
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# Once variables have been chosen, it is good to optimize #
# the hyper-parameters.  This script will do that.        #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from Options import Options

from sklearn import grid_search
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score

from sklearn.ensemble import GradientBoostingClassifier

#-----------------------------------------------------#
# Perform grid search on development data
#-----------------------------------------------------#
def gridSearch(dt_dev, dt_eval, opts):

    # Make the BDT classifier
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),    
                             algorithm = 'SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)
    
    # Setup the parameter grid to scan
    pgrid = {"n_estimators": [100,200,300,400,500,800,1000],
             "base_estimator__max_depth": [2,3,4,5,6,7],
             #"max_depth": [2,3,4,5,6],
             "learning_rate": [0.1,0.3,0.5,0.7,0.9,1.1,1.3]
         }
    
    # Now setup the grid search
    gsearch = grid_search.GridSearchCV(bdt, pgrid, cv=3,
                                       scoring='roc_auc',
                                       n_jobs=6)

    # Fit dat shit
    _ = gsearch.fit(dt_dev.getDataNoWeight(), dt_dev.targets)

    # Print the results of the search
    # Copied http://betatim.github.io/posts/advanced-sklearn-for-TMVA/
    print "Best parameter set found on development set:"
    print
    print gsearch.best_estimator_
    print
    print "Grid scores on a subset of the development set:"
    print
    for params, mean_score, scores in gsearch.grid_scores_:
        print "%0.4f (+/-%0.04f) for %r"%(mean_score, scores.std(), params)
    print
    print "With the model trained on the full development set:"
    
    y_true, y_pred = dt_dev.targets, gsearch.decision_function(dt_dev.getDataNoWeight())
    print "  It scores %0.4f on the full development set"%roc_auc_score(y_true, y_pred)
    y_true, y_pred = dt_eval.targets, gsearch.decision_function(dt_eval.getDataNoWeight())
    print "  It scores %0.4f on the full evaluation set"%roc_auc_score(y_true, y_pred)
    
