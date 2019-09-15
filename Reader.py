import os
import pickle
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
            for i in range (0, 5):
                for j in range (0,4):
                    currentBone = gestureData[i,j,:]
                    xBaseNotYetScaled = currentBone[0]
                    yBaseNotYetScaled = currentBone[1]

                    xTipNotYetScaled = currentBone[3]
                    yTipNotYetScaled = currentBone[4]
                    print xBaseNotYetScaled,yBaseNotYetScaled,xTipNotYetScaled,yTipNotYetScaled


            self.Draw_Gestures()
    def Draw_Gestures(self):
        while True:
            self.Draw_Each_Gesture_Once()
    def Draw_Each_Gesture_Once(self):
        for num in range(1, self.gestureNum + 1):

            self.Draw_Gesture(num)
    def Draw_Gesture(self, i ):
        print i
        self.pygameWindow.Prepare()
        self.pygameWindow.Reveal()
    def ScalePygameValue(self,oldValue, oldMin, oldMax, newMin, newMax):
        self.oldRange = (oldMax - oldMin)
        if oldRange == 0:
            newValue = newMin
        else:
            newRange = (newMax - newMin)
            newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
        return newValue





