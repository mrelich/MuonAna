
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

f_data    = 'trees/Data_BS_Sep9_L3Applied.root'

print "Loading data..."
dt_data    = ReadData(f_data, m_sname_data, "")

dt_out = dt_data.data

labels = dt_data.treenames + dt_data.w_varnames + m_weightnames

csl = ""
for i in range(len(labels)-1):
    csl += labels[i] + ","
csl += labels[-1]

dt_out = np.rec.fromrecords(dt_out, names=csl)

basename = 'total_withweights_morevars'
dataname  = 'processed_trees/' + basename + '_data.root'

array2root(dt_out, dataname, 'tree','recreate')
