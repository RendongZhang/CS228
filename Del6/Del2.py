import sys

sys.path.insert(0, '../..')
import Leap
from Leap import Finger
from Leap import Bone

import pickle
from pygameWindow import PYGAME_WINDOW
import numpy as np
import constants

clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')



x = 100
y = 100
width = 10
pygameWindow = PYGAME_WINDOW()



def Handle_Frame(frame):
    global x,y,xMin,xMax,yMin,yMax,testData
    hand = frame.hands[0]


    fingers = hand.fingers
    global k
    k = 0
    for i in range(5):
        finger = hand.fingers[i]
        Handle_Finger(finger)

    testData = CenterData(testData)  #13a


    predictedClass = clf.Predict(testData)
    print "predict : " , predictedClass


    indexFingerList = hand.fingers.finger_type(Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]

    distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[1])


    if (x < xMin):
        xMin = x
    if (x > xMax):
        xMax = x
    if (y < yMin):
        yMin = y
    if (y > yMax):
        yMax = y

def Handle_Finger(finger):
    global width
    width = 10
    for b in range(0, 4):

        Handle_Bone(finger.bone(b),b)

        width = width - 2



def Handle_Bone(bone,b):
    global k
    base = bone.prev_joint
    tip = bone.next_joint
    baseCo = Handle_Vector_From_Leap(base)
    tipCo = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseCo,tipCo,width)

    if ((b == 0) or (b == 3)):
        testData[0, k] = int(bone.next_joint.x)
        testData[0, k + 1] = int(bone.next_joint.y)
        testData[0, k + 2] = int(bone.next_joint.z)
        k = k + 3
def CenterData(data):
    allDataCoordinates = data[0, ::3]
    meanValue = allDataCoordinates.mean()
    data[0, ::3] = allDataCoordinates - meanValue
    allDataCoordinates = data[0,1::3]
    meanValue = allDataCoordinates.mean()
    data[0,1::3] = allDataCoordinates - meanValue
    allDataCoordinates = data[0, 2::3]
    meanValue = allDataCoordinates.mean()
    data[0, 2::3] = allDataCoordinates - meanValue
    return data


def Handle_Vector_From_Leap(v):
    x = int(ScalePygameValue(int(v[0]),xMin,xMax,0, constants.pygameWindowWidth))
    y = int(ScalePygameValue(int(v[2]),yMin,yMax,0, constants.pygameWindowDepth))
    return x, y


def ScalePygameValue(oldValue,oldMin,oldMax,newMin,newMax):
    oldRange = (oldMax - oldMin)
    if oldRange == 0:
        newValue = newMin

    else:
        newRange = (newMax - newMin)
        newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin

    return newValue



controller = Leap.Controller()
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    handlist = frame.hands
    for hand in handlist:
        if (len(str(hand)) > 0):

            Handle_Frame(frame)

    pygameWindow.Reveal()


