
# My things
from MyData import Data, ReadData
from Constants import *
from Options import Options
from Tools import split_data

# Options to be used
from TMVATest import tmvatest
from GridSearch import gridSearch
from Validation import kvalidation
from MethodExplore import explore
from SaveInfo import savemodel, savedata
from Evaluate import evaluate
from PlotEffArea import ploteffarea
from nMinus1Check import n1check

from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib

# Generic
import numpy as np
from optparse import OptionParser

#---------------------------------------------------#
# Load options to decide what we will run
#---------------------------------------------------#

parser = OptionParser()
parser.add_option("--validation",action="store_true",
                  default=False, dest="validation",
                  help="Run k-fold validation")
parser.add_option("--tmvatest", action="store_true",
                  default=False, dest="tmvatest",
                  help="Run TMVA like test")
parser.add_option("--evaluate", action="store_true",
                  default=False, dest="evaluate",
                  help="Run over the evaluation data and save plot")
parser.add_option("--gridsearch", action="store_true",
                  default=False, dest="gridsearch",
                  help="Grid search")
parser.add_option("--explore", action="store_true",
                  default=False, dest="explore",
                  help="Look at other methods besides BDT")
parser.add_option("--savemodel",action="store_true",
                  default=False, dest="savemodel",
                  help="Save the trained model")
parser.add_option("--savedata",action="store_true",
                  default=False, dest="savedata",
                  help="Save the data not used in training")
parser.add_option("--ploteffarea",action="store_true",
                  default=False, dest="ploteffarea",
                  help="Plot Effective area")
parser.add_option("--n1check",action="store_true",
                  default=False, dest="n1check",
                  help="Check against some baseline the results of removing a variable")
parser.add_option("--model", action="store",
                  default="", dest="modelpath",
                  help="Specify an input path to a pickled model")
parser.add_option("--bdtopt", action="store", type=int,
                  default=0, dest="bdtopt",
                  help="Specify bdt option. See Options.py for details")

options, args = parser.parse_args()

#---------------------------------------------------#
# Setup the Options object
#---------------------------------------------------#

print "BDT Option:  ", options.bdtopt
print "Model input: ", options.modelpath

opts = Options(bdtopt = options.bdtopt,
               modelin = options.modelpath)

#---------------------------------------------------#
# Prepare the data
#---------------------------------------------------#

# Load Data
d_sig = ReadData(opts.fsig, m_sname_E2, opts.cuts+"&&"+opts.sigcut)
d_bkg = ReadData(opts.fbkg, m_sname_corsika, opts.cuts)

# Mix the simulation
#X_total = np.concatenate((d_sig.data, d_bkg.data),axis=0)
#y_total = np.concatenate((d_sig.targets, d_bkg.targets),axis=0)

# Create a total data obj
#d_tot = Data(X_total,y_total,"total")

# Get development and evaluation datasets
#d_dev, d_eval = split_data(X_total,y_total,
#                           tr_size=opts.devfrac,
#                           rnd_state=2212457,
#                           name="devsplit",
#                           w_train = 1./opts.devfrac,
#                           w_test = 1./(1-opts.devfrac))

# Get training and test set from the dev set 
# Remember weight factor is now a fraction of 
# the amount passed in!
#d_trn, d_tst  = split_data(d_dev.data,d_dev.targets,
#                           tr_size=opts.trainfrac,
#                           rnd_state=49122,
#                           name="trainsplit",
#                           w_train = 1./(opts.devfrac*opts.trainfrac),
#                           w_test  = 1./((1-opts.devfrac)*(1-opts.trainfrac)))

# Get training and development sets for signal
sig_X_dev, sig_X_eval, sig_y_dev, sig_y_eval = train_test_split(d_sig.data,
                                                                d_sig.targets,
                                                                train_size = opts.devfrac,
                                                                random_state=2212457)
sig_X_trn, sig_X_tst, sig_y_trn, sig_y_tst = train_test_split(sig_X_dev,
                                                              sig_y_dev,
                                                              train_size = opts.trainfrac,
                                                              random_state=2212457)

# Get training and development sets for data
bkg_X_dev, bkg_X_eval, bkg_y_dev, bkg_y_eval = train_test_split(d_bkg.data,
                                                                d_bkg.targets,
                                                                train_size = opts.devfrac,
                                                                random_state=2212457)
bkg_X_trn, bkg_X_tst, bkg_y_trn, bkg_y_tst = train_test_split(bkg_X_dev,
                                                              bkg_y_dev,
                                                              train_size = opts.trainfrac,
                                                              random_state=2212457)


# Now combine signal and bkg into dev, eval, trn, and tst
def combine(Xsig,Xbkg,ysig,ybkg,name,sf):
    return Data(np.concatenate((Xsig,Xbkg),axis=0),
                np.concatenate((ysig,ybkg),axis=0),
                name,
                sf)

d_tot = combine(d_sig.data,d_bkg.data,d_sig.targets,d_bkg.targets,"tot",1)

d_dev = combine(sig_X_dev,bkg_X_dev,sig_y_dev,bkg_y_dev,"dev",
                1/opts.devfrac)
d_eval = combine(sig_X_eval,bkg_X_eval,sig_y_eval,bkg_y_eval,"eval",
                 1/(1-opts.devfrac))
d_trn = combine(sig_X_trn,bkg_X_trn,sig_y_trn,bkg_y_trn,"trn",
                1./(opts.devfrac*opts.trainfrac))
d_tst = combine(sig_X_tst,bkg_X_tst,sig_y_tst,bkg_y_tst,"tst",
                1./((1-opts.devfrac)*(1-opts.trainfrac)))

#---------------------------------------------------#
# Determine which option to run
#---------------------------------------------------#

# Perform TMVA like test of correlations and
# comparisons for testing and training set
if options.tmvatest: 
    tmvatest(d_tot,d_trn,d_tst,opts)

# Perform the grid search
if options.gridsearch: 
    gridSearch(d_dev, d_eval, opts)

# Perform validation using parameters in Options.py
if options.validation:
    kvalidation(d_dev, opts, k=3, njobs=2)

# Check some other methods and see if there is any benefit
if options.explore:
    explore(d_trn, d_tst)

# Save the trained model which can then be used later
if options.savemodel:
    savemodel(d_dev, opts)

# Save the data
if options.savedata:
    
    if len(opts.modelinput) != 0:
        clf = joblib.load(opts.modelinput)
        savedata(d_eval,"testing",clf)
    else:
        savedata(d_eval,"testing")

# Run over the evaluation data set
if options.evaluate:
    evaluate(d_eval,d_dev,opts)

# Plot effective area
if options.ploteffarea:
    ploteffarea(d_eval,d_dev,opts)

# Check results of bdt by removing 1 variable
if options.n1check:
    n1check(d_trn, d_tst, opts)
