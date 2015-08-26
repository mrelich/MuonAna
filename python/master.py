
# My things
from MyData import Data, ReadData
from Constants import *
import Options as opts
from Tools import split_data

# Options to be used
from TMVATest import tmvatest
from GridSearch import gridSearch
from Validation import kvalidation

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
                  help="Evaluate bdt and save")
parser.add_option("--gridsearch", action="store_true",
                  default=False, dest="gridsearch",
                  help="Grid search")

options, args = parser.parse_args()

#---------------------------------------------------#
# Prepare the data
#---------------------------------------------------#

# Load Data
d_sig = ReadData(opts.fsig, m_sname_E2, opts.cuts+"&&"+opts.sigcut)
d_bkg = ReadData(opts.fbkg, m_sname_corsika, opts.cuts)

# Mix the simulation
X_total = np.concatenate((d_sig.data, d_bkg.data),axis=0)
y_total = np.concatenate((d_sig.targets, d_bkg.targets),axis=0)

# Create a total data obj
d_tot = Data(X_total,y_total,"total")

# Get development and evaluation datasets
d_dev, d_eval = split_data(X_total,y_total,
                           tr_size=opts.devfrac,
                           rnd_state=2212457,
                           name="devsplit",
                           w_train = 1./opts.devfrac,
                           w_test = 1./(1-opts.devfrac))

# Get training and test set from the dev set 
# Remember weight factor is now a fraction of 
# the amount passed in!
d_trn, d_tst  = split_data(d_dev.data,d_dev.targets,
                           tr_size=opts.trainfrac,
                           rnd_state=49122,
                           name="trainsplit",
                           w_train = 1./(opts.devfrac*opts.trainfrac),
                           w_test  = 1./((1-opts.devfrac)*(1-opts.trainfrac)))

#---------------------------------------------------#
# Determine which option to run
#---------------------------------------------------#

# Perform TMVA like test of correlations and
# comparisons for testing and training set
if options.tmvatest: 
    tmvatest(d_tot,d_trn,d_tst)

# Perform the grid search
if options.gridsearch: 
    gridSearch(d_dev, d_eval)

# Perform validation using parameters in Options.py
if options:
    kvalidation(d_dev, k=3, njobs=2)
