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


pickle_in = open('userData/Childs_train0.p', "rb")
train0 = pickle.load(pickle_in)
pickle_in.close()
train0 = ReduceData(train0)
train0 = CenterData(train0)
pickle_in = open('userData/Newton_train1.p', "rb")
train1 = pickle.load(pickle_in)
pickle_in.close()
train1 = ReduceData(train1)
train1 = CenterData(train1)
pickle_in = open('userData/Apple_train2.p', "rb")
train2 = pickle.load(pickle_in)
pickle_in.close()
train2 = ReduceData(train2)
train2 = CenterData(train2)
pickle_in = open('userData/Beatty_train3.p', "rb")
train3 = pickle.load(pickle_in)
pickle_in.close()
train3 = ReduceData(train3)
train3 = CenterData(train3)
pickle_in = open('userData/Ortigara_train4.p', "rb")
train4 = pickle.load(pickle_in)
pickle_in.close()
train4 = ReduceData(train4)
train4 = CenterData(train4)
pickle_in = open('userData/Ortigara_train5.p', "rb")
train5 = pickle.load(pickle_in)
pickle_in.close()
train5 = ReduceData(train5)
train5 = CenterData(train5)
pickle_in = open('userData/Boland_train6.p', "rb")
train6 = pickle.load(pickle_in)
pickle_in.close()
train6 = ReduceData(train6)
train6 = CenterData(train6)
pickle_in = open('userData/Huang_train7.p', "rb")
train7 = pickle.load(pickle_in)
pickle_in.close()
train7 = ReduceData(train7)
train7 = CenterData(train7)
pickle_in = open('userData/Erickson_train8.p', "rb")
train8 = pickle.load(pickle_in)
pickle_in.close()
train8 = ReduceData(train8)
train8 = CenterData(train8)
pickle_in = open('userData/Soccorsi_train9.p', "rb")
train9 = pickle.load(pickle_in)
pickle_in.close()
train9 = ReduceData(train9)
train9 = CenterData(train9)


pickle_in = open('userData/Childs_test0.p', "rb")
test0 = pickle.load(pickle_in)
pickle_in.close()
test0 = ReduceData(test0)
test0 = CenterData(test0)
pickle_in = open('userData/Newton_test1.p', "rb")
test1 = pickle.load(pickle_in)
pickle_in.close()
test1 = ReduceData(test1)
test1 = CenterData(test1)
pickle_in = open('userData/Apple_test2.p', "rb")
test2 = pickle.load(pickle_in)
pickle_in.close()
test2 = ReduceData(test2)
test2 = CenterData(test2)
pickle_in = open('userData/Beatty_test3.p', "rb")
test3 = pickle.load(pickle_in)
pickle_in.close()
test3 = ReduceData(test3)
test3 = CenterData(test3)
pickle_in = open('userData/Ortigara_test4.p', "rb")
test4 = pickle.load(pickle_in)
pickle_in.close()
test4 = ReduceData(test4)
test4 = CenterData(test4)
pickle_in = open('userData/Ortigara_test5.p', "rb")
test5 = pickle.load(pickle_in)
pickle_in.close()
test5 = ReduceData(test5)
test5 = CenterData(test5)
pickle_in = open('userData/Boland_test6.p', "rb")
test6 = pickle.load(pickle_in)
pickle_in.close()
test6 = ReduceData(test6)
test6 = CenterData(test6)
pickle_in = open('userData/Huang_test7.p', "rb")
test7 = pickle.load(pickle_in)
pickle_in.close()
test7 = ReduceData(test7)
test7 = CenterData(test7)
pickle_in = open('userData/Erickson_test8.p', "rb")
test8 = pickle.load(pickle_in)
pickle_in.close()
test8 = ReduceData(test8)
test8 = CenterData(test8)
pickle_in = open('userData/Soccorsi_test9.p', "rb")
test9 = pickle.load(pickle_in)
pickle_in.close()
test9 = ReduceData(test9)
test9 = CenterData(test9)


def ReshapeData(set0, set1, set2, set3, set4, set5, set6, set7, set8, set9):
    X = np.zeros((10000, 5 * 2 * 3), dtype='f')
    y = np.zeros(10000, dtype='f')
    for row in range(0, 1000):
        col = 0
        y[row] = 0
        y[row + 1000] = 1
        y[row + 2000] = 2
        y[row + 3000] = 3
        y[row + 4000] = 4
        y[row + 5000] = 5
        y[row + 6000] = 6
        y[row + 7000] = 7
        y[row + 8000] = 8
        y[row + 9000] = 9
        for finger in range(0, 5):
            for bone in range(0, 2):
                for m in range(0, 3):
                    X[row,        col] = set0[finger, bone, m, row]
                    X[row + 1000, col] = set1[finger, bone, m, row]
                    X[row + 2000, col] = set2[finger, bone, m, row]
                    X[row + 3000, col] = set3[finger, bone, m, row]
                    X[row + 4000, col] = set4[finger, bone, m, row]
                    X[row + 5000, col] = set5[finger, bone, m, row]
                    X[row + 6000, col] = set6[finger, bone, m, row]
                    X[row + 7000, col] = set7[finger, bone, m, row]
                    X[row + 8000, col] = set8[finger, bone, m, row]
                    X[row + 9000, col] = set9[finger, bone, m, row]

                    col = col + 1
    return X, y


trainX, trainy = ReshapeData(train0, train1, train2, train3, train4, train5, train6, train7, train8, train9)
testX, testy = ReshapeData(test0, test1, test2, test3, test4, test5, test6, test7, test8, test9)

knn = knn.KNN()
knn.Use_K_Of(15)
counter = 0
knn.Fit(trainX, trainy)
# for row in range(0, 10000):
#     prediction = int(knn.Predict(testX[row]))
#     if (prediction == int(testy[row])):
#         counter += 1

#print (float(counter) / 10000)
pickle.dump(knn, open('userData/classifier.p', 'w'))
