
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# Set of tools to make things simpler in the main #
# sections of code... basicaly for cleanliness.   #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from MyData import Data
from sklearn.cross_validation import train_test_split

#----------------------------------#
# Split data into test and train
# but keeping things in my data
# format  
#----------------------------------#
def split_data(X,y,tr_size,rnd_state,name,w_train,w_test):
    X_trn, X_tst, y_trn, y_tst = train_test_split(X,y,
                                                  train_size = tr_size,
                                                  random_state = rnd_state)
    train = Data(X_trn,y_trn,name+"_trn",w_train)
    test  = Data(X_tst,y_tst,name+"_tst",w_test)
    return train,test

