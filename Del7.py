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

clf = pickle.load(open('Del6/userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')

x = 0
y = 0
width = 10
pygameWindow = PYGAME_WINDOW()


def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax, testData, predictedClass
    hand = frame.hands[0]

    fingers = hand.fingers
    global k
    k = 0
    for i in range(5):
        finger = hand.fingers[i]
        Handle_Finger(finger)

    testData = CenterData(testData)  # 13a

    predictedClass = clf.Predict(testData)
    print "predict : ", predictedClass

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
    global k, programState, centered, seconds

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
        # print("success", programState)
        if programState == 1:
            pygameWindow.screen.blit(imageSuccess, (constants.pygameWindowWidth / 2, 0))

            seconds += 1
            print ("seconds ", seconds)
            if seconds >= 200:
                programState = 2
                pass
    if programState == 2:
        pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        # pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        seconds = 0
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
    global predictedClass, programState, randomNum, imageNumber, imageASL, wrongTimes, wrongPredict, correct, correctTimes,allNumber
    global correctPredict
    # print (predictedClass, randomNum)
    if (len(handlist) == 0):
        programState = 0
    if (len(handlist) > 0 and centered == False):
        programState = 1
        pass

    if predictedClass == randomNum and predictedClass != 11 and correctTimes <= 6  and correctPredict < 10:
        correctPredict += 1
        print correctTimes, "correct 1 situation"
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)
        if database[userName]['digit{0}attempted'.format(randomNum)] >= 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        elif   2 <= database[userName]['digit{0}attempted'.format(randomNum)] < 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            if  2 < correctPredict < 6:
                pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))

        elif  database[userName]['digit{0}attempted'.format(randomNum)] <2:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        programState = 3
        pass
    if predictedClass == randomNum and correctTimes <= 6 and correctPredict >= 10:
        print correctTimes, "correct 2 situation"
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)
        correctPredict = 0
        wrongTimes = 0
        wrongPredict = 0
        correctTimes += 1
        correct.add(randomNum)
        print correctTimes,"correct 1 situation"

        if database[userName]['digit{0}attempted'.format(randomNum)] >= 4:
            pygameWindow.screen.blit(imageCorrect, (constants.pygameWindowWidth / 2, 0))
        elif   2 <= database[userName]['digit{0}attempted'.format(randomNum)] < 4:
            pygameWindow.screen.blit(imageCorrect, (constants.pygameWindowWidth / 2, 0))
            if  2 < correctPredict < 6:
                pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))


        elif  database[userName]['digit{0}attempted'.format(randomNum)] <2:
            pygameWindow.screen.blit(imageCorrect, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))


        database[userName]["digit{0}attempted".format(randomNum)] += 1
        # pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))


        lis = list(correct)
        randomNum = lis[random.randint(0, len(lis)-1)]
        imageNumber = pygame.image.load('number/{0}.jpeg'.format(randomNum))
        imageNumber = pygame.transform.scale(imageNumber,
                                             (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        imageASL = pygame.image.load('number/ASL{0}.png'.format(randomNum))
        imageASL = pygame.transform.scale(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        programState = 2
        s0 = ("Digit 0 presented : " + str(database[userName]['digit0attempted']))
        s1 = ("Digit 1 presented : " + str(database[userName]['digit1attempted']))
        s2 = ("Digit 2 presented : " + str(database[userName]['digit2attempted']))
        s3 = ("Digit 3 presented : " + str(database[userName]['digit3attempted']))
        s4 = ("Digit 4 presented : " + str(database[userName]['digit4attempted']))
        s5 = ("Digit 5 presented : " + str(database[userName]['digit5attempted']))
        s6 = ("Digit 6 presented : " + str(database[userName]['digit6attempted']))
        s7 = ("Digit 7 presented : " + str(database[userName]['digit7attempted']))
        s8 = ("Digit 8 presented : " + str(database[userName]['digit8attempted']))
        s9 = ("Digit 9 presented : " + str(database[userName]['digit9attempted']))
        text0 = font.render(s0, True, (0, 128, 0))
        text1 = font.render(s1, True, (0, 128, 0))
        text2 = font.render(s2, True, (0, 128, 0))
        text3 = font.render(s3, True, (0, 128, 0))
        text4 = font.render(s4, True, (0, 128, 0))
        text5 = font.render(s5, True, (0, 128, 0))
        text6 = font.render(s6, True, (0, 128, 0))
        text7 = font.render(s7, True, (0, 128, 0))
        text8 = font.render(s8, True, (0, 128, 0))
        text9 = font.render(s9, True, (0, 128, 0))
        pygameWindow.screen.blit(text0, (0, 400))
        pygameWindow.screen.blit(text1, (0, 440))
        pygameWindow.screen.blit(text2, (0, 480))
        pygameWindow.screen.blit(text3, (0, 520))
        pygameWindow.screen.blit(text4, (0, 560))
        pygameWindow.screen.blit(text5, (0, 600))
        pygameWindow.screen.blit(text6, (0, 640))
        pygameWindow.screen.blit(text7, (0, 680))
        pygameWindow.screen.blit(text8, (0, 720))
        pygameWindow.screen.blit(text9, (0, 760))

        pygame.display.update()
        pygame.event.get()

        print "delay"
        time.sleep(2)
        pass
    if predictedClass == randomNum and predictedClass != 11 and correctTimes > 6  and correctPredict < 10:
        correctPredict += 1
        print correctTimes, "correct 3 situation"
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)

        if database[userName]['digit{0}attempted'.format(randomNum)] >= 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        elif 2 <= database[userName]['digit{0}attempted'.format(randomNum)] < 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))

        elif database[userName]['digit{0}attempted'.format(randomNum)] < 2:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        programState = 3
        pass
    if predictedClass == randomNum and correctTimes > 6 and correctPredict >= 10:
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)
        print correctTimes, "correct 4 situation"
        wrongTimes = 0
        wrongPredict = 0
        correctTimes = 0
        correct.add(randomNum)
        pygameWindow.screen.blit(imageCorrect, (constants.pygameWindowWidth / 2, 0))
        database[userName]["digit{0}attempted".format(randomNum)] += 1
        # pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        dif = allNumber - correct
        if len(dif) > 0:
            diff = list(dif)
            randomNum = diff[0]
            correct.add(randomNum)
            lis = list(correct)
            randomNum = lis[random.randint(0,len(lis)-1)]
        else :
            randomNum = lis[random.randint(0,len(lis)-1)]
        imageNumber = pygame.image.load('number/{0}.jpeg'.format(randomNum))
        imageNumber = pygame.transform.scale(imageNumber,
                                             (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        imageASL = pygame.image.load('number/ASL{0}.png'.format(randomNum))
        imageASL = pygame.transform.scale(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
        programState = 2
        s0 = ("Digit 0 presented : " + str(database[userName]['digit0attempted']))
        s1 = ("Digit 1 presented : " + str(database[userName]['digit1attempted']))
        s2 = ("Digit 2 presented : " + str(database[userName]['digit2attempted']))
        s3 = ("Digit 3 presented : " + str(database[userName]['digit3attempted']))
        s4 = ("Digit 4 presented : " + str(database[userName]['digit4attempted']))
        s5 = ("Digit 5 presented : " + str(database[userName]['digit5attempted']))
        s6 = ("Digit 6 presented : " + str(database[userName]['digit6attempted']))
        s7 = ("Digit 7 presented : " + str(database[userName]['digit7attempted']))
        s8 = ("Digit 8 presented : " + str(database[userName]['digit8attempted']))
        s9 = ("Digit 9 presented : " + str(database[userName]['digit9attempted']))
        text0 = font.render(s0, True, (0, 128, 0))
        text1 = font.render(s1, True, (0, 128, 0))
        text2 = font.render(s2, True, (0, 128, 0))
        text3 = font.render(s3, True, (0, 128, 0))
        text4 = font.render(s4, True, (0, 128, 0))
        text5 = font.render(s5, True, (0, 128, 0))
        text6 = font.render(s6, True, (0, 128, 0))
        text7 = font.render(s7, True, (0, 128, 0))
        text8 = font.render(s8, True, (0, 128, 0))
        text9 = font.render(s9, True, (0, 128, 0))
        pygameWindow.screen.blit(text0, (0, 400))
        pygameWindow.screen.blit(text1, (0, 440))
        pygameWindow.screen.blit(text2, (0, 480))
        pygameWindow.screen.blit(text3, (0, 520))
        pygameWindow.screen.blit(text4, (0, 560))
        pygameWindow.screen.blit(text5, (0, 600))
        pygameWindow.screen.blit(text6, (0, 640))
        pygameWindow.screen.blit(text7, (0, 680))
        pygameWindow.screen.blit(text8, (0, 720))
        pygameWindow.screen.blit(text9, (0, 760))

        pygame.display.update()
        pygame.event.get()

        print "delay"
        time.sleep(2)

        pass
    elif predictedClass == 11:
        programState = 4
        pygameWindow.screen.blit(imageSeeYou, (0, 0))
        pygame.display.update()
        pygame.event.get()
        time.sleep(3)
        pass
    elif predictedClass != randomNum and predictedClass != 11  and wrongPredict < 10:
        wrongPredict += 1
        print wrongTimes, "wrong 1 situation"
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)

        if database[userName]['digit{0}attempted'.format(randomNum)] >= 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
        elif 2 <= database[userName]['digit{0}attempted'.format(randomNum)] < 4:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            if 2 < wrongPredict < 6:
                pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))

        elif database[userName]['digit{0}attempted'.format(randomNum)] < 2:
            pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        programState = 3
        pass
    elif predictedClass != randomNum and predictedClass != 11  and wrongPredict >=10:
        wrongPredict = 0
        # wrongTimes += 1
        print wrongTimes, "wrong 2 situation"
        for hand in handlist:
            if (len(str(hand)) > 0):
                Handle_Frame(frame)


        if database[userName]['digit{0}attempted'.format(randomNum)] >= 4:
            pygameWindow.screen.blit(imageWrong, (constants.pygameWindowWidth / 2, 0))
        elif   2 <= database[userName]['digit{0}attempted'.format(randomNum)] < 4:
            pygameWindow.screen.blit(imageWrong, (constants.pygameWindowWidth / 2, 0))
            if 2 < wrongPredict < 6:
                pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))

        elif  database[userName]['digit{0}attempted'.format(randomNum)] <2:
            pygameWindow.screen.blit(imageWrong, (constants.pygameWindowWidth / 2, 0))
            pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))


        pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
        pygame.display.update()
        pygame.event.get()

        programState = 3


        pass
    # elif predictedClass != randomNum and predictedClass != 11 and wrongTimes >= 5 and wrongPredict != 10:
    #     wrongPredict += 1
    #     print wrongTimes, "wrong 3 situation"
    #     for hand in handlist:
    #         if (len(str(hand)) > 0):
    #             Handle_Frame(frame)
    #
    #     pygameWindow.screen.blit(imageNumber, (constants.pygameWindowWidth / 2, 0))
    #     pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
    #
    #     programState = 3
    #     pass
    # elif predictedClass != randomNum and predictedClass != 11 and wrongTimes >= 5 and wrongPredict == 10:
    #     wrongPredict = 0
    #     wrongTimes += 1
    #     print wrongTimes, "wrong 4 situation"
    #     for hand in handlist:
    #         if (len(str(hand)) > 0):
    #             Handle_Frame(frame)
    #
    #     pygameWindow.screen.blit(imageWrong, (constants.pygameWindowWidth / 2, 0))
    #     pygameWindow.screen.blit(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowWidth / 2))
    #
    #     programState = 3
    #     pygame.display.update()
    #     pygame.event.get()
    #
    #     pass




allNumber = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
correct = set([])
correctTimes = 0
correctPredict = 0
wrongPredict = 0
wrongTimes = 0
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
imageSeeYou = pygame.image.load("number/seeyou.png")
imageSeeYou = pygame.transform.scale(imageSeeYou, (constants.pygameWindowWidth, constants.pygameWindowDepth))
#
randomNum = 0
imageNumber = pygame.image.load('number/{0}.jpeg'.format(randomNum))
imageNumber = pygame.transform.scale(imageNumber, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
imageASL = pygame.image.load('number/ASL{0}.png'.format(randomNum))
imageASL = pygame.transform.scale(imageASL, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))
#
font = pygame.font.SysFont("comicsansms", 48)

database = database = pickle.load(open('userData/database.p', 'rb'))
userName = raw_input('Please enter your name: ')
if userName in database:
    database[userName]['logins'] += 1
    print('welcome back ' + userName + '.')
    print 'Your  successful attempts: '
    print "Digit 0 : ", database[userName]['digit0attempted']
    print "Digit 1 : ", database[userName]['digit1attempted']
    print "Digit 2 : ", database[userName]['digit2attempted']
    print "Digit 3 : ", database[userName]['digit3attempted']
    print "Digit 4 : ", database[userName]['digit4attempted']
    print "Digit 5 : ", database[userName]['digit5attempted']
    print "Digit 6 : ", database[userName]['digit6attempted']
    print "Digit 7 : ", database[userName]['digit7attempted']
    print "Digit 8 : ", database[userName]['digit8attempted']
    print "Digit 9 : ", database[userName]['digit9attempted']
else:
    database[userName] = {'logins': 1, 'digit0attempted': 0, 'digit1attempted': 0, 'digit2attempted': 0,
                          'digit3attempted': 0, 'digit4attempted': 0, 'digit5attempted': 0, 'digit6attempted': 0,
                          'digit7attempted': 0, 'digit8attempted': 0, 'digit9attempted': 0}
    print('welcome ' + userName + '.')
    print('Your  successful attempts: ')
    print "Digit 0 : ", database[userName]['digit0attempted']
    print "Digit 1 : ", database[userName]['digit1attempted']
    print "Digit 2 : ", database[userName]['digit2attempted']
    print "Digit 3 : ", database[userName]['digit3attempted']
    print "Digit 4 : ", database[userName]['digit4attempted']
    print "Digit 5 : ", database[userName]['digit5attempted']
    print "Digit 6 : ", database[userName]['digit6attempted']
    print "Digit 7 : ", database[userName]['digit7attempted']
    print "Digit 8 : ", database[userName]['digit8attempted']
    print "Digit 9 : ", database[userName]['digit9attempted']

pygame.display.set_caption('ASL Game')
predictedClass = -1
centered = False
programState = 0
seconds = 0
loop = True
while loop:
    pygameWindow.Prepare()
    frame = controller.frame()
    handlist = frame.hands

    if (programState == 0):
        HandleState0()
    elif (programState == 1):
        HandleState1()
    elif (programState == 2):
        HandleState2()
    elif (programState == 3):
        HandleState3()
    elif (programState == 4):
        loop = False

    pygameWindow.Reveal()

pygame.quit()

pickle.dump(database, open('userData/database.p', 'wb'))
print("Game Over")
