import sys
import os
import glob
import pickle
import numpy as np
sys.path.insert(0, '..')
import Leap
from Leap import Finger
from Leap import Bone
import constants
from pygameWindow_Del03 import PYGAME_WINDOW
class DELIVERABLE:
    def __init__(self):
        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.x = 100
        self.y = 100
        self.xMin = -100.0
        self.xMax = 100.0
        self.yMin = -100.0
        self.yMax = 100.0
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5, 4, 6), dtype='f')
        self.gesNumber = 1
        self.Empty_Directory()
    def Empty_Directory(self):
        files = glob.glob('userData/*')
        for f in files:
            os.remove(f)

    def Handle_Frame(self,frame):

        hand = frame.hands[0]
        fingers = hand.fingers
        for i in range(5):
            finger = hand.fingers[i]
            self.Handle_Finger(finger,i)
        indexFingerList = hand.fingers.finger_type(Finger.TYPE_INDEX)
        indexFinger = indexFingerList[0]
        distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
        tip = distalPhalanx.next_joint
        x = int(tip[0])
        y = int(tip[1])
        if x < self.xMin:
            self.xMin = x
        if x > self.xMax:
            self.xMax = x
        if y < self.yMin:
            self.yMin = y
        if y > self.yMax:
            self.yMax = y

        if self.Recording_Is_Ending():
            print(self.gestureData)
            self.Save_Gesture(self.gesNumber)
            self.gesNumber += 1
    def Save_Gesture(self,gesNumber):
        pickle_out = open('userData/gesture{0}.txt'.format(self.gesNumber),"wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()
    def Recording_Is_Ending(self):
        if (self.previousNumberOfHands == 2) and (self.currentNumberOfHands == 1):
            return True
        else:
            return False
    def Handle_Finger(self,finger,i):
        global width
        width = 10
        for b in range(0, 4):
            self.Handle_Bone(finger.bone(b),i,b)
            width = width - 2
    def Handle_Bone(self,bone,i,j):
        base = bone.prev_joint
        tip = bone.next_joint
        baseCo = self.Handle_Vector_From_Leap(base)
        tipCo = self.Handle_Vector_From_Leap(tip)
        if (self.currentNumberOfHands == 1):
            self.pygameWindow.Draw_Line(baseCo, tipCo, width,(0,255,0))
        if (self.currentNumberOfHands == 2):
            self.pygameWindow.Draw_Line(baseCo, tipCo, width, (255, 0, 0))
        if self.Recording_Is_Ending():
            self.gestureData[i, j, 0] = bone.prev_joint.x
            self.gestureData[i, j, 1] = bone.prev_joint.y
            self.gestureData[i, j, 2] = bone.prev_joint.z
            self.gestureData[i, j, 3] = bone.next_joint.x
            self.gestureData[i, j, 4] = bone.next_joint.y
            self.gestureData[i, j, 5] = bone.next_joint.z

    def Handle_Vector_From_Leap(self,v):

        x = int(self.ScalePygameValue(int(v[0]), self.xMin, self.xMax, 0, constants.pygameWindowWidth))
        y = int(self.ScalePygameValue(int(v[2]), self.yMin, self.yMax, 0, constants.pygameWindowDepth))

        return x, y
    def ScalePygameValue(self,oldValue, oldMin, oldMax, newMin, newMax):
        oldRange = (oldMax - oldMin)
        if oldRange == 0:
            newValue = newMin
        else:
            newRange = (newMax - newMin)
            newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
        return newValue
    def Run_Forever(self):

        while True:
            self.Run_Once()

    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = self.controller.frame()

        handlist = frame.hands

        self.currentNumberOfHands = len(handlist)


        for hand in handlist:


            if len(str(hand)) > 0:
                self.Handle_Frame(frame)

        self.pygameWindow.Reveal()
        self.previousNumberOfHands = self.currentNumberOfHands
