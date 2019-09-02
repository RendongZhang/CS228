import sys

sys.path.insert(0, '..')
import Leap
from Leap import Finger
from Leap import Bone
import random
from pygameWindow import PYGAME_WINDOW




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
    global x,y
    hand = frame.hands[0]
    print(hand)

    fingers = hand.fingers

    indexFingerList = hand.fingers.finger_type(Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    print(indexFinger)
    distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[1])
    
    print(type(tip))
    print(tip)
    print(x)
    print(y)

controller = Leap.Controller()
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    handlist = frame.hands

    for hand in handlist:
        if (len(str(hand)) > 0):
            Handle_Frame(frame)

    pygameWindow.Draw_Black_Circle(x,y)
    Perturb_Circle_Position()
    pygameWindow.Reveal()


