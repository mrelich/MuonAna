
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# A quick way to add the weights to the root files for simple plotting  #
# later.                                                                #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#


from MyData import ReadData, Data
from SaveInfo import savedata
from Constants import *
from Options import Options
import numpy as np

opts = Options()

f_nugen   = 'trees/NuGen_10634_Sep10_L3Applied.root'
f_corsika = 'trees/Corsika_11362_Sep10_L3Applied.root'
f_data    = 'trees/Data_BS_Sep9_L3Applied.root'
f_corsikaLE = 'trees/Corsika_11499_Sep10_L3Applied_LECorsika.root'

# Load NuGen
print "Loading NuGen..."
dt_nugen   = ReadData(f_nugen, m_sname_E2, opts.sigcut)

# Load Low Energy NuGen
print "Loading NuGen LE..."
dt_nugenLE = ReadData(f_nugen, m_sname_E2, "!"+opts.sigcut)

# Load Corsika and low enegy corsika
print "Loading Corsika..."
dt_corsika   = ReadData(f_corsika, m_sname_corsika, "")
dt_corsikaLE = ReadData(f_corsikaLE, m_sname_corsikaLE, "")

# combine
dt_corsika = Data(np.concatenate((dt_corsika.data,dt_corsikaLE.data),axis=0),
                  np.concatenate((dt_corsika.targets,dt_corsikaLE.targets),axis=0),
                  "totalCorsika",
                  1)



print "Loading data..."
dt_data    = ReadData(f_data, m_sname_data, "")
#dt_data = None

#print dt_nugen.data
#print dt_nugenLE.data
#print dt_corsika.data

dt_total = Data(np.concatenate((dt_nugen.data,dt_corsika.data),axis=0),
                np.concatenate((dt_nugen.targets,dt_corsika.targets),axis=0),
                "total",
                1)

print "Saving..."
savedata(dt_total, dt_nugenLE, "total_withweights", None, dt_data)
