
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# File containing the options for how to divide the data into training #
# and evaluating sample as well as the BDT options for the final use.  #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

import os, sys

class Options:

    # Constructor
    def __init__(self, 
                 fsig       = "trees/NuGen_11069_Sep14_L3Applied.root",
                 fbkg       = "trees/Corsika_11362_Sep10_L3Applied.root",
                 sigcut     = "(log10(nuE)>=6)",
                 devfrac    = 0.8,
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
            
            self.cuts = "(1)"
            
            self.ntrees   = 500
            self.lrate    = 0.1
            self.maxdepth = 3
            self.minsamplesplit = 5000
            
            self.bdtname  = "adaboostminsplit5k"

        elif(bdtopt == 1):                         # passL3Muon
            
            self.cuts = "(1)"
            
            self.ntrees   = 500
            self.lrate    = 0.1
            self.maxdepth = 3
            self.minsamplesplit = 2
            
            self.bdtname  = "adaboostminsplit2"

        elif(bdtopt == 2):                         # passL3Muon
            
            self.cuts = "(spline_mpe_zen >= -999 && cos(spline_mpe_zen) < 0.2)"
            
            self.ntrees   = 500
            self.lrate    = 0.1
            self.maxdepth = 3
            self.minsamplesplit = 5
            
            self.bdtname  = "adaboostminsplit2_upgoing"

        elif(bdtopt == 3):                         # passL3Muon - up going
            
            self.cuts = "(spline_mpe_zen >= -999 && cos(spline_mpe_zen) < 0.2)"
            
            self.ntrees   = 500
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 5000
                        
            self.bdtname  = "adaboostminsplit5k_upgoing"

        elif(bdtopt == 4):                         # passL3Muon - down going
            
            self.cuts = "(1)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 2

            self.bdtname  = "adaboostminsplit2_800tree"

        elif(bdtopt == 5):                         # passL3Muon - down going
            
            self.cuts = "(1)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 5000

            self.bdtname  = "adaboostminsplit5k_800tree"

        elif(bdtopt == 6):                         # passL3Muon - down going
            
            self.cuts = "(1)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 10000

            self.bdtname  = "adaboostminsplit10k_800tree"

        elif(bdtopt == 7):                         # passL3Muon - down going
            
            self.cuts = "(spline_mpe_zen >= -999 && cos(spline_mpe_zen) < 0.2)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 10000

            self.bdtname  = "adaboostminsplit10k_upgoing_800tree"

        elif(bdtopt == 8):                         # passL3Muon - down going
            
            self.cuts = "(1)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 7
            self.minsamplesplit = 5

            self.bdtname  = "adaboostminsplit5_800tree"

        elif(bdtopt == 9):                         # passL3Muon - down going
            
            self.cuts = "(spline_mpe_zen >= -999 && cos(spline_mpe_zen) < 0.2)"
            
            self.ntrees   = 800
            self.lrate    = 0.1
            self.maxdepth = 6
            self.minsamplesplit = 10000

            self.bdtname  = "adaboostminsplit10k_upgoing_800tree_maxdepth6"



        else:                                      # Model isn't specified
            print "BDT option is not supported"
            print "Please look in Options.py"
            sys.exit()
        

