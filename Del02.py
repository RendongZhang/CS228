import sys

sys.path.insert(0, '..')
import Leap
from Leap import Finger
from Leap import Bone
import random
from pygameWindow import PYGAME_WINDOW
import constants

x = 450
y = 300

pygameWindow = PYGAME_WINDOW()

def Perturb_Circle_Position():
    global x, y
    fourSidedDieRoll = random.randint(1,4)
    if fourSidedDieRoll == 1 :
        x = x - 1
    elif fourSidedDieRoll == 2 :
        x = x + 1
    elif fourSidedDieRoll == 3 :
        y = y - 1
    elif fourSidedDieRoll == 4 :
        y = y + 1

def Handle_Frame(frame):
    global x,y,xMin,xMax,yMin,yMax
    hand = frame.hands[0]


    fingers = hand.fingers

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


def ScalePygameValue(oldValue,oldMin,oldMax,newMin,newMax,axis):
    oldRange = (oldMax - oldMin)
    if oldRange == 0:
        newValue = newMin

    else:
        newRange = (newMax - newMin)
        newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    if axis == "x":
        return int(newValue)
    else:
        return (newMax-int(newValue))


controller = Leap.Controller()
xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    handlist = frame.hands
    pygameX = constants.pygameWindowWidth/2
    pygameY = constants.pygameWindowDepth/2
    for hand in handlist:
        if (len(str(hand)) > 0):
            Handle_Frame(frame)
            pygameX = ScalePygameValue(x, xMin, xMax, 0, constants.pygameWindowWidth,"x")
            pygameY = ScalePygameValue(y, yMin, yMax, 0, constants.pygameWindowDepth,"y")

            #print(pygameX,pygameY)

    pygameWindow.Draw_Black_Circle(pygameX,pygameY)

    Perturb_Circle_Position()
    pygameWindow.Reveal()


