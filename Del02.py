import sys

sys.path.insert(0, '..')
import Leap
from Leap import Finger
from Leap import Bone
import random
from pygameWindow import PYGAME_WINDOW

import constants

x = 100
y = 100
width = 10
pygameWindow = PYGAME_WINDOW()



def Handle_Frame(frame):
    global x,y,xMin,xMax,yMin,yMax
    hand = frame.hands[0]


    fingers = hand.fingers

    for i in range(5):
        finger = hand.fingers[i]
        Handle_Finger(finger)


    # finger2 =
    # bone = finger1.bone(Bone.TYPE_PROXIMAL)


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

        Handle_Bone(finger.bone(b))

        width = width - 2
        # original  8 c  bone = finger.bone(b)

def Handle_Bone(bone):
    base = bone.prev_joint
    tip = bone.next_joint
    baseCo = Handle_Vector_From_Leap(base)
    tipCo = Handle_Vector_From_Leap(tip)

    pygameWindow.Draw_Black_Line(baseCo,tipCo,width)

def Handle_Vector_From_Leap(v):
    print(int(v[0]),int(v[2]))

    x = int(ScalePygameValue(int(v[0]),xMin,xMax,0, constants.pygameWindowWidth))
    y = int(ScalePygameValue(int(v[2]),yMin,yMax,0, constants.pygameWindowDepth))
    print(x,y)
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


