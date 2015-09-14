
# My things
from MyData import Data, ReadData
from Constants import *
from Options import Options
from Tools import split_data

# Options to be used
from TMVATest import tmvatest
from GridSearch import gridSearch
from Validation import kvalidation, k3validplot
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
parser.add_option("--validationplots",action="store_true",
                  default=False, dest="validationplots",
                  help="Run k-fold validation plots")
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
parser.add_option("--savename",action="store",
                  default="testing", dest="savename",
                  help="Save the data not used in training to this filename")
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

# Get training and development sets for signal
sig_X_dev, sig_X_eval, sig_y_dev, sig_y_eval = train_test_split(d_sig.data,
                                                                d_sig.targets,
                                                                train_size = opts.devfrac,
                                                                random_state=2212457)
sig_X_trn, sig_X_tst, sig_y_trn, sig_y_tst = train_test_split(sig_X_dev,
                                                              sig_y_dev,
                                                              train_size = opts.trainfrac,
                                                              random_state=2212457)

print "---------------------------------------------------"
print "Signal: "
print "Development: ", len(sig_X_dev)
print "Evaluate:    ", len(sig_X_eval)

# Get training and development sets for data
bkg_X_dev, bkg_X_eval, bkg_y_dev, bkg_y_eval = train_test_split(d_bkg.data,
                                                                d_bkg.targets,
                                                                train_size = opts.devfrac,
                                                                random_state=2212457)
bkg_X_trn, bkg_X_tst, bkg_y_trn, bkg_y_tst = train_test_split(bkg_X_dev,
                                                              bkg_y_dev,
                                                              train_size = opts.trainfrac,
                                                              random_state=2212457)

print "---------------------------------------------------"
print "Background:"
print "Development: ", len(bkg_X_dev)
print "Evaluate:    ", len(bkg_X_eval)


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

#**********************************************#
# Perform TMVA like test of correlations and
# comparisons for testing and training set
#**********************************************#
if options.tmvatest: 
    tmvatest(d_tot,d_trn,d_tst,opts)

#**********************************************#
# Perform the grid search
#**********************************************#
if options.gridsearch: 
    gridSearch(d_dev, d_eval, opts)

#**********************************************#
# Perform validation using parameters 
# in Options.py
#**********************************************#
if options.validation:
    kvalidation(d_dev, opts, k=3, njobs=2)

if options.validationplots:
    k3validplot(d_dev, opts)

#**********************************************#
# Check some other methods and see if there 
# is any benefit
#**********************************************#
if options.explore:
    explore(d_trn, d_tst)

#**********************************************#
# Save the trained model which can then 
# be used later
#**********************************************#
if options.savemodel:
    savemodel(d_dev, opts)

#**********************************************#
# Save the data
#**********************************************#
if options.savedata:
    
    # Check if model is set
    if len(opts.modelinput) == 0:
        print "Please specify the input model to run"
        print "Otherwise this process of saving scores"
        print "will take too long."
        sys.exit()

    # Read in the low energy data as well
    d_LE = ReadData(opts.fsig, m_sname_E2, opts.cuts+"&&!"+opts.sigcut)

    # Load classifier
    clf = joblib.load(opts.modelinput)

    # save data
    savedata(d_eval, d_LE, options.savename, clf)

#**********************************************#
# Run over the evaluation data set
#**********************************************#
if options.evaluate:
    evaluate(d_eval,d_dev,opts)

#**********************************************#
# Plot effective area
#**********************************************#
if options.ploteffarea:
    
    # Add in the low energy data as well
    d_LE = ReadData(opts.fsig, m_sname_E2, opts.cuts+"&&!"+opts.sigcut)

    # Add it to the evaluation data
    ploteffarea(d_eval,d_dev,opts,d_LE)

#**********************************************#
# Check results of bdt by removing 1 variable
#**********************************************#
if options.n1check:
    n1check(d_trn, d_tst, opts)
