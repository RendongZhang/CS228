import numpy as np
import pickle

pickle_in = open('userData/train7.dat', "rb")
trainM = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open('userData/train8.dat', "rb")
trainN = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open('userData/test7.dat', "rb")
testM = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open('userData/test8.dat', "rb")
testN = pickle.load(pickle_in)
pickle_in.close()

def ReshapeData(set1,set2):
    X = np.zeros((2000, 5 * 4 * 6), dtype='f')
    y = np.zeros(2000,dtype='f')
    for row in range(0, 1000):
        col = 0
        y[row] = 7
        y[row+1000]=8
        for finger in range(0, 5):
            for bone in range(0, 4):
                for m in range(0, 6):
                    X[row, col] = set1[finger, bone, m, row]
                    X[row+1000, col] = set2[finger, bone, m, row]
                    col = col + 1
    return X, y
trainX, trainy= ReshapeData(trainM,trainN)
testX, testy = ReshapeData(testM, testN)
print trainX
print trainX.shape
print trainy
print trainy.shape
print testX
print testX.shape
print testy
print testy.shape

