
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# File containing the options for how to divide the data into training #
# and evaluating sample as well as the BDT options for the final use.  #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Files to read in from
fsig = "trees/NuGen_10634_Aug24.root"
fbkg = "trees/Corsika_11362_Aug24.root"

# Specific cuts to be used when extracting data
cuts = "passL3Muon&&cos(spline_mpe_zen)<0.2"
sigcut = "log10(nuE)>=6"

# How to split the data
devfrac   = 0.33  # This will be used for training and testing
trainfrac = 0.5   # XX% of development fraction to be used for training

# BDT parameters
ntrees   = 200
lrate    = 0.5
maxdepth = 3

