
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# File containing the options for how to divide the data into training #
# and evaluating sample as well as the BDT options for the final use.  #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

import os, sys

class Options:

    # Constructor
    def __init__(self, 
                 #fsig = "trees/NuGen_10634_Aug24.root",
                 #fbkg       = "trees/Corsika_11362_Aug24.root",
                 fsig       = "trees/NuGen_10634_Aug31.root",
                 fbkg       = "trees/Corsika_11362_Aug31.root",
                 sigcut     = "(log10(nuE)>=6)",
                 #devfrac    = 0.33,
                 devfrac    = 0.5,
                 trainfrac  = 0.5,
                 bdtopt     = 0,
                 modelin    = ""):

        # Store files
        self.fsig = fsig
        self.fbkg = fbkg
        
        # Store signal cut
        self.sigcut = sigcut
        
        # Store info for how to split datasets
        self.devfrac   = devfrac
        self.trainfrac = trainfrac

        # If user chose to use model already generated
        # Save it here if it exists
        if len(modelin) != 0 and not os.path.exists(modelin):
            print "Model path specified does not exist."
            print "Exiting"
            sys.exit()
        self.modelinput = modelin

        # BDT options should be the best fit for
        # a specific set of reco-cuts
        if(bdtopt == 0):                         # passL3Muon
            
            self.cuts = "passL3Muon"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 6
            
            self.bdtname  = "adaboost"

        elif(bdtopt == 1):                         # passL3Muon - up going
            
            self.cuts = "passL3Muon&&cos(spline_mpe_zen)<0.2"
            
            self.ntrees   = 1000
            self.lrate    = 1.3
            self.maxdepth = 7
            
            self.bdtname  = "adaboost_upgoing"

        elif(bdtopt == 2):                         # passL3Muon - down going
            
            self.cuts = "passL3Muon&&cos(spline_mpe_zen)>=0.2"
            
            self.ntrees   = 1000
            self.lrate    = 1.3
            self.maxdepth = 7
            
            self.bdtname  = "adaboost_downgoing"

        else:                                      # Model isn't specified
            print "BDT option is not supported"
            print "Please look in Options.py"
            sys.exit()
        

