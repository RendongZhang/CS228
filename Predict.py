import matplotlib.pyplot as plt
import knn
import numpy as np

knn = knn.KNN()
knn.Load_Dataset('iris.csv')
x = knn.data[:, 0]
y = knn.data[:, 1]

trainX = knn.data[::2, 1:3]
trainy = knn.target[::2]
testX = knn.data[1::2, 1:3]
testy = knn.target[1::2]

knn.Use_K_Of(15)
knn.Fit(trainX, trainy)
for j in range(0,75):
    actualClass = testy[j]
    prediction = knn.Predict(testX[j, 1:3])

plt.figure()
colors = np.zeros((3,3),dtype='f')
colors[0,:] = [1,0.5,0.5]
colors[1,:] = [0.5,1,0.5]
colors[2,:] = [0.5,0.5,1]
[numItems,numFeatures] = knn.data.shape
for i in range(0,numItems/2):
    itemClass = int(trainy[i])
    currColor = colors[itemClass, :]
    plt.scatter(trainX[i,0],trainX[i,1], facecolor = currColor, s= 50, lw=2,edgecolors="black")
count = 0

for k in range(0,numItems/2):
    prediction = int(knn.Predict(testX[k, :]))
    edgeColor = colors[prediction, :]
    itemClass = int(testy[k])
    if prediction == itemClass:
        count += 1
    currColor = colors[itemClass, :]
    plt.scatter(testX[k, 0], testX[k, 1], facecolor=currColor, s=50,  lw=2, edgecolor=edgeColor)


plt.show()
print (count)
print (float(count) / len(testX) *100)

