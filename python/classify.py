
# My things
from MyData import Data, ReadData
from Constants import *
import Options as opts

# Generic
import numpy as np

# Import BDT stuff
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split

# Load Data
d_sig = ReadData(opts.fsig, m_sname_E2, opts.cuts+"&&"+opts.sigcut)
d_bkg = ReadData(opts.fbkg, m_sname_corsika, opts.cuts)

# Mix the simulation
X_total = np.concatenate((d_sig.data, d_bkg.data),axis=0)
y_total = np.concatenate((d_sig.targets, d_bkg.targets),axis=0)

# Wrapper to keep using my data format 
# which is useful for weights
def split_data(X,y,tr_size,rnd_state,name):
    X_trn, X_tst, y_trn, y_tst = train_test_split(X,y,
                                                  train_size = tr_size,
                                                  random_state = rnd_state)
    train = Data(X_trn,y_trn,name+"_trn")
    test  = Data(X_tst,y_tst,name+"_tst")
    return train,test

# Get the training set
#d_dev, d_eval = split_data(X_total,y_total,
#                           tr_size=opts.devfrac,
#                           rnd_state=42,
#                           name="devsplit")
#d_trn, d_tst  = split_data(d_dev.data,d_dev.targets,
#                           tr_size=opts.trainfrac,
#                           rnd_state=42,
#                           name="trainsplit")
d_trn, d_tst  = split_data(X_total, y_total,
                           tr_size=opts.devfrac,
                           rnd_state=42,
                           name="trainsplit")

print len(d_trn.data), len(d_tst.data)

# Make BDT
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),    
                         algorithm = 'SAMME',
                         n_estimators=opts.ntrees,
                         learning_rate=opts.lrate)

print "Fitting data"
bdt.fit(d_trn.getDataNoWeight(), d_trn.targets)

print "Evaluating"
pred = bdt.decision_function(d_tst.getDataNoWeight())
#pred_eval = bdt.decision_function(d_eval.getDataNoWeight())

# Import ROOT stuff and save
from ROOT import TH1F, TFile
h_sig = TH1F("h_sig","h",100,-1,1)
h_bkg = TH1F("h_bkg","h",100,-1,1)
h_sig_eval = TH1F("h_sig_eval","h",100,-1,1)
h_bkg_eval = TH1F("h_bkg_eval","h",100,-1,1)

# fill hist
weights = d_tst.getDataWeights()
for i in range(len(pred)):
    if d_tst.targets[i]: 
        h_sig.Fill(pred[i],weights[i])
    else:
        h_bkg.Fill(pred[i],weights[i])
#weights = d_eval.getDataWeights()
#for i in range(len(pred_eval)):
#    if d_eval.targets[i]:
#        h_sig_eval.Fill(pred_eval[i],weights[i])
#    else:
#        h_bkg_eval.Fill(pred_eval[i],weights[i])

# write to file
output = TFile("test2_PeV.root","recreate")
output.cd()
h_sig.Write()
h_bkg.Write()
#h_sig_eval.Write()
#h_bkg_eval.Write()
output.Write()
output.Close()
