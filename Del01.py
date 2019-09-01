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

while True:
    pygameWindow.Prepare()
    pygameWindow.Draw_Black_Circle(x,y)
    Perturb_Circle_Position()
    pygameWindow.Reveal()


