import os
import time
import pickle
import constants
from pygameWindow_Del03 import PYGAME_WINDOW
import numpy as np

class READER:
    def __init__(self):

        self.gestureNum = self.Gesture_Number()
        self.pygameWindow = PYGAME_WINDOW()
    def Gesture_Number(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)
        return self.numGestures
    def Print_Gestures(self):
        # pickle_in = open('userData/gesture{0}.txt'.format(gestureNum), "rb")
        # gestureData = pickle.load(pickle_in)
        # pickle_in.close()
        for num in range(1, self.gestureNum + 1):
            pickle_in = open('userData/gesture{0}.txt'.format(num), "rb")
            gestureData = pickle.load(pickle_in)
            pickle_in.close()
            print(gestureData)
            for i in range (0, 5):
                for j in range (0,4):
                    currentBone = gestureData[i,j,:]
                    # xBaseNotYetScaled = currentBone[0]
                    xBase = int(self.ScalePygameValue(currentBone[0]))
                    # yBaseNotYetScaled = currentBone[1]
                    yBase = int(self.ScalePygameValue(currentBone[1]))
                    # xTipNotYetScaled = currentBone[3]
                    xTip = int(self.ScalePygameValue(currentBone[3]))
                    # yTipNotYetScaled = currentBone[4]
                    yTip = int(self.ScalePygameValue(currentBone[4]))
                    self.pygameWindow.Draw_Line((xBase,xTip), (yBase, yTip), 5 ,(0,0,255))




    def Draw_Gestures(self):
        while True:
            self.Draw_Each_Gesture_Once()

    def Draw_Each_Gesture_Once(self):
        for num in range(1, self.gestureNum + 1):

            self.Draw_Gesture(num)

    def Draw_Gesture(self, i ):

        self.pygameWindow.Prepare()
        pickle_in = open('userData/gesture{0}.txt'.format(i), "rb")
        gestureData = pickle.load(pickle_in)
        pickle_in.close()

        for i in range(0, 5):
            for j in range(0, 4):
                currentBone = gestureData[i, j, :]
                # xBaseNotYetScaled = currentBone[0]
                # print currentBone[0],currentBone[1],currentBone[3],currentBone[4]
                xBase = int(self.ScalePygameValue(currentBone[0]))

                # yBaseNotYetScaled = currentBone[1]
                yBase = int(self.ScalePygameValue(currentBone[2]))
                # xTipNotYetScaled = currentBone[3]
                xTip = int(self.ScalePygameValue(currentBone[3]))
                # yTipNotYetScaled = currentBone[4]
                yTip = int(self.ScalePygameValue(currentBone[5]))
                # print(xBase,yBase,xTip,xTip)
                self.pygameWindow.Draw_Line((xBase, yBase), (xTip, yTip), 1, (0, 0, 255))
        time.sleep(0.5)
        self.pygameWindow.Reveal()

    def ScalePygameValue(self,oldValue):
        oldRange = (constants.maxValue - constants.minValue)
        newMin = 0
        newMax = constants.pygameWindowDepth
        if oldRange == 0:
            newValue = newMin
        else:
            newRange = (newMax - newMin)
            newValue = (((oldValue - constants.minValue) * newRange) / oldRange) + newMin
        # if axis == "x":
        #     return int(newValue)
        # else:
        #     return (newMax - int(newValue))
        return newValue




