import sys

import pygame

sys.path.insert(0, '..')
import Leap
from Leap import Finger
from Leap import Bone

import pickle
from pygameWindow import PYGAME_WINDOW
import numpy as np
import constants
import random
import time
import matplotlib.pyplot as plt

clf = pickle.load( open('Del6/userData/classifier.p','rb') )
testData = np.zeros((1, 30), dtype='f')

x = 0
y = 0
width = 10
pygameWindow = PYGAME_WINDOW()


def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax, testData,predictedClass
    hand = frame.hands[0]

    fingers = hand.fingers
    global k
    k = 0
    for i in range(5):
        finger = hand.fingers[i]
        Handle_Finger(finger)

    testData = CenterData(testData)  # 13a

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
        Handle_Bone(finger.bone(b), b)

        width = width - 2


def Handle_Bone(bone, b):
    global k, programState, centered,seconds

    base = bone.prev_joint
    tip = bone.next_joint
    baseCo = Handle_Vector_From_Leap(base)
    tipCo = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseCo, tipCo, width)
    if ((b == 0) or (b == 3)):
        testData[0, k] = int(bone.next_joint.x)
        testData[0, k + 1] = int(bone.next_joint.y)
        testData[0, k + 2] = int(bone.next_joint.z)
        k = k + 3

    if baseCo[0] < 60:
        centered = False
        print("left", programState)
        if programState == 1:
            pygameWindow.screen.blit(imageLeft, (constants.pygameWindowWidth / 2, 0))
        seconds = 0
        pass
    if baseCo[0] > 440:
        centered = False
        if programState == 1:
            pygameWindow.screen.blit(imageRight, (constants.pygameWindowWidth / 2, 0))
        print("Right", programState)
        seconds = 0
        pass
    if baseCo[1] < 40:
        centered = False
        print("High", programState)
        if programState == 1:
            pygameWindow.screen.blit(imageHigh, (constants.pygameWindowWidth / 2, 0))
        seconds = 0
        pass
    # print("y", baseCo[1])
    if baseCo[1] > 320:
        centered = False
        print("Low", programState)
        if programState == 1:
            pygameWindow.screen.blit(imageLow, (constants.pygameWindowWidth / 2, 0))
        seconds = 0
        pass

    if baseCo[0] < 60 or baseCo[0] > 440 or baseCo[1] < 40 or baseCo[1] > 320:
        centered = False
        programState = 1
        seconds = 0
        pass
    if 60 < baseCo[0] < 440 and 40 < baseCo[1] < 320:
        centered = True
        print("success",programState)
        if programState == 1:
            pygameWindow.screen.blit(imageSuccess, (constants.pygameWindowWidth / 2, 0))

            seconds += 1
            print ("seconds ", seconds)
            if seconds >= 100:

                programState = 2
                pass
    if programState ==2:

        pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2,constants.pygameWindowWidth / 2 ))

        programState = 3
        pass




def CenterData(data):
    allDataCoordinates = data[0, ::3]
    meanValue = allDataCoordinates.mean()
    data[0, ::3] = allDataCoordinates - meanValue
    allDataCoordinates = data[0, 1::3]
    meanValue = allDataCoordinates.mean()
    data[0, 1::3] = allDataCoordinates - meanValue
    allDataCoordinates = data[0, 2::3]
    meanValue = allDataCoordinates.mean()
    data[0, 2::3] = allDataCoordinates - meanValue
    return data


def Handle_Vector_From_Leap(v):
    x = int(ScalePygameValue(int(v[0]), xMin, xMax, 0, constants.pygameWindowWidth / 2))
    y = int(ScalePygameValue(int(v[2]), yMin, yMax, 0, constants.pygameWindowDepth / 2))

    return x, y


def ScalePygameValue(oldValue, oldMin, oldMax, newMin, newMax):
    oldRange = (oldMax - oldMin)
    if oldRange == 0:
        newValue = newMin

    else:
        newRange = (newMax - newMin)
        newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    return newValue


def HandleState0():
    global programState
    pygameWindow.screen.blit(image, (0, 0))
    if len(handlist) > 0:
        programState = 1


def HandleState1():
    global programState

    if len(handlist) == 0:
        programState = 0
    for hand in handlist:
        if (len(str(hand)) > 0):
            Handle_Frame(frame)


def HandleState2():
    global programState, centered
    if (len(handlist) == 0):
        programState = 0
    if (len(handlist) > 0 and centered == False):
        programState = 1
        pass

    # print "programstate: ", programState, "centered: ", centered
    for hand in handlist:
        if (len(str(hand)) > 0):
            Handle_Frame(frame)
def HandleState3():
    global  predictedClass,programState,randomNum,imageNumber,imageASL
    print (predictedClass,randomNum)
    if (len(handlist) == 0):
        programState = 0
    if (len(handlist) > 0 and centered == False):
        programState = 1
        pass

    if (predictedClass == randomNum ):

        pygameWindow.screen.blit(imageCorrect, (constants.pygameWindowWidth / 2, 0))
        pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        randomNum = random.randint(0, 9)
        imageNumber = pygame.image.load('number/{0}.jpeg'.format(randomNum))
        imageNumber = pygame.transform.scale(imageNumber,  (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        imageASL = pygame.image.load('number/ASL{0}.png'.format(randomNum))
        imageASL = pygame.transform.scale(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        programState = 2
        pygame.display.update()
        pygame.event.get()
        print "delay"
        time.sleep(2)

        pass
    elif (predictedClass != randomNum ):
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)

        pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))

        programState = 3
        pass



controller = Leap.Controller()
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0
image = pygame.image.load('hoverYourHand.jpg')
image = pygame.transform.scale(image, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageLeft = pygame.image.load('tooleft.jpeg')
imageLeft = pygame.transform.scale(imageLeft, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageRight = pygame.image.load('tooright.jpeg')
imageRight = pygame.transform.scale(imageRight, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageHigh = pygame.image.load('toohigh.jpeg')
imageHigh = pygame.transform.scale(imageHigh, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageLow = pygame.image.load('toolow.jpeg')
imageLow = pygame.transform.scale(imageLow, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageSuccess = pygame.image.load('succeed.jpeg')
imageSuccess = pygame.transform.scale(imageSuccess, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageCorrect = pygame.image.load("number/correct.jpeg")
imageCorrect = pygame.transform.scale(imageCorrect, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageWrong = pygame.image.load("number/wrong.jpeg")
imageWrong = pygame.transform.scale(imageWrong, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
#
randomNum = random.randint(0,9)
imageNumber = pygame.image.load('number/{0}.jpeg'.format(randomNum))
imageNumber = pygame.transform.scale(imageNumber, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageASL= pygame.image.load('number/ASL{0}.png'.format(randomNum))
imageASL = pygame.transform.scale(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))



pygame.display.set_caption('ASL Game')
predictedClass = -1
centered = False
programState = 0
seconds = 0
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    handlist = frame.hands

    if (programState == 0):
        HandleState0()
    elif (programState == 1):
        HandleState1()
    elif (programState == 2):
        HandleState2()
    elif (programState == 3 ):
        HandleState3()

    pygameWindow.Reveal()
