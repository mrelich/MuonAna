
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# This script is meant to mimic the use of TMVA for consistency #
# checks as well as some useful figures for evaluating over     #
# training.                                                     #
#                                                               #
# Some of the plotting methods taken from Tim's tutorial:       #
# http://betatim.github.io/posts/sklearn-for-TMVA-users/        #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from MyData import Data
import Options as opts
import numpy as np

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc

import pandas as pd
import pandas.core.common as com
from pandas.core.index import Index

from pandas.tools import plotting
from pandas.tools.plotting import scatter_matrix

import matplotlib.pyplot as plt

#------------------------------------------------#
# Correlation plots
#------------------------------------------------#
def correlations(data, sname, **kwds):
    corrmat = data.corr(**kwds)
    
    fig, ax1 = plt.subplots(ncols=1, figsize=(7,6))
    
    opts = {'cmap': plt.get_cmap("RdBu"),
            'vmin': -1, 'vmax': +1}
    heatmap1 = ax1.pcolor(corrmat, **opts)
    plt.colorbar(heatmap1, ax=ax1)
    
    ax1.set_title("Correlations")
    
    labels = corrmat.columns.values
    for ax in (ax1,):
        # shift location of ticks to center of the bins
        ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
        ax.set_yticklabels(labels, minor=False)
        
    plt.tight_layout()
    #plt.show()
    plt.savefig("plots/tmvatest/"+sname+".eps")
    

#------------------------------------------------#
# Use training and testing set to make standard
# comparison for overtraining
#------------------------------------------------#
def test_train_ROC(bdt, dt_train, dt_test):

    # Test performace and print some useful info
    dt_test_noW = dt_test.getDataNoWeight()
    predicted = bdt.predict(dt_test_noW)
    print classification_report(dt_test.targets, predicted,
                                target_names=["background","signal"])
    
    test_dec_func =  bdt.decision_function(dt_test_noW)
    print "Area on ROC curve: %.4f"%(roc_auc_score(dt_test.targets, test_dec_func))

    # Save the ROC as well
    fpr, tpr, thresholds = roc_curve(dt_test.targets, test_dec_func)
    roc_auc = auc(fpr,tpr)
    
    # New figure
    fig, ax1 = plt.subplots(ncols=1, figsize=(7,6))

    plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)'%(roc_auc))
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.grid()
    #plt.show()
    
    plt.savefig("plots/tmvatest/ROC.eps")

#------------------------------------------------#
# Simple overtraining comp
#------------------------------------------------#
def test_train_compare(bdt, dt_train, dt_test, bins=30):

    # Now plot the training and test samples on same figure
    # to check for over-training
    fig1, ax1 = plt.subplots(ncols=1, figsize=(7,6))
    decisions = []
    for X,y in ((dt_train.getDataNoWeight(), dt_train.targets),
                (dt_test.getDataNoWeight(), dt_test.targets)):
        d1 = bdt.decision_function(X[y>0.5]).ravel()
        d2 = bdt.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]
        
    # Save min and max for x-axis
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)

    # Create nice filled histogram of signal -- train
    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')
    
    # Create nice filled histogram of background --train
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')

    # Now make standard histogram of signal -- test
    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, normed=True)
    
    # Set Error info
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
    
    # Now make standard histogram of background -- test
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')
    ax1.set_ylim(bottom=0)
    plt.show()
    
    # Save
    plt.savefig("plots/tmvatest/overtrain_check.eps")
    

#------------------------------------------------#
# Method to make plots as are done in TMVA
#------------------------------------------------#
def tmvatest(dt_total, dt_train, dt_test):


    # Use panda data format for the plots
    pdt_tot = pd.DataFrame(np.hstack((dt_total.getDataNoWeight(),
                                      dt_total.targets.reshape(dt_total.targets.shape[0],-1))),
                           columns=dt_total.l_varnames+['y'])    
    
    # Set cuts for sig and bkg
    csig = pdt_tot.y > 0.5
    cbkg = pdt_tot.y < 0.5

    # Plot correlations
    #correlations(pdt_tot[cbkg].drop('y',1),"var_cor_bkg")
    #correlations(pdt_tot[csig].drop('y',1),"var_cor_sig")

    # Make BDT -- here we will use the options
    # specified in Options.py
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),    
                             algorithm = 'SAMME',
                             n_estimators=opts.ntrees,
                             learning_rate=opts.lrate)

    # Train and test BDT
    bdt.fit(dt_train.getDataNoWeight(), dt_train.targets)

    # Make comparison figures for test and training
    #test_train_ROC(bdt, dt_train, dt_test)
    
    # Do the simple over-training check
    test_train_compare(bdt, dt_train, dt_test)
