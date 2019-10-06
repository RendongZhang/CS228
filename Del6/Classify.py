import numpy as np
import pickle
import knn


def ReduceData(X):

    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)

    return X
def CenterData(X):
    allXCoordinates = X[:, :, 0, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 0, :] = allXCoordinates - meanValue
    allXCoordinates = X[:, :, 1, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 1, :] = allXCoordinates - meanValue
    allXCoordinates = X[:, :, 2, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 2, :] = allXCoordinates - meanValue
    return X
pickle_in = open('userData/train7.dat', "rb")
trainM = pickle.load(pickle_in)
pickle_in.close()
trainM = ReduceData(trainM)
trainM = CenterData(trainM)

pickle_in = open('userData/train8.dat', "rb")
trainN = pickle.load(pickle_in)
pickle_in.close()
trainN = ReduceData(trainN)
trainN = CenterData(trainN)

pickle_in = open('userData/test7.dat', "rb")
testM = pickle.load(pickle_in)
pickle_in.close()
testM = ReduceData(testM)
testM =CenterData(testM)

pickle_in = open('userData/test8.dat', "rb")
testN = pickle.load(pickle_in)
pickle_in.close()
testN = ReduceData(testN)
testN = CenterData(testN)

def ReshapeData(set1,set2):
    X = np.zeros((2000, 5 * 2 * 3), dtype='f')
    y = np.zeros(2000,dtype='f')
    for row in range(0, 1000):
        col = 0
        y[row] = 7
        y[row+1000]=8
        for finger in range(0, 5):
            for bone in range(0, 2):
                for m in range(0, 3):
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


knn = knn.KNN()
knn.Use_K_Of(15)
counter = 0
knn.Fit(trainX, trainy)
for row in range(0,2000):
    prediction = int(knn.Predict(testX[row]))
    if (prediction == int(testy[row])):
        counter += 1

print (float(counter)/2000)
pickle.dump(knn, open('userData/classifier.p','wb'))