import sys
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
    def Handle_Frame(self,frame):
        self.x, self.y, self.xMin, self.xMax, self.yMin, self.yMax
        hand = frame.hands[0]
        fingers = hand.fingers
        for i in range(5):
            finger = hand.fingers[i]
            self.Handle_Finger(finger)
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
    def Handle_Finger(self,finger):
        global width
        width = 10
        for b in range(0, 4):
            self.Handle_Bone(finger.bone(b))
            width = width - 2
    def Handle_Bone(self,bone):
        base = bone.prev_joint
        tip = bone.next_joint
        baseCo = self.Handle_Vector_From_Leap(base)
        tipCo = self.Handle_Vector_From_Leap(tip)
        self.pygameWindow.Draw_Black_Line(baseCo, tipCo, width)
    def Handle_Vector_From_Leap(self,v):
        print(int(v[0]), int(v[2]))
        x = int(self.ScalePygameValue(int(v[0]), self.xMin, self.xMax, 0, constants.pygameWindowWidth))
        y = int(self.ScalePygameValue(int(v[2]), self.yMin, self.yMax, 0, constants.pygameWindowDepth))
        print(x, y)
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
        for hand in handlist:
            if (len(str(hand)) > 0):
                self.Handle_Frame(frame)
        self.pygameWindow.Reveal()