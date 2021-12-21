"""
In this version of the game, there shouldn't be any lag buffered double input fuckery
but the issue is that spamming keys won't make it faster anymore.
"""
from time import *
import pygame as pg
from pygame.locals import *

from __level__ import *

#List of control keys
ContKeys = [K_BACKSPACE, K_RCTRL, K_UP, K_RIGHT, K_DOWN, K_LEFT, K_SPACE, K_RETURN, K_KP_PLUS, K_ESCAPE]

def isKeyPressed(pressedKeys) :
    """
    Returns True if a control key is pressed,
    False if not.
    """
    global ContKeys
    for key in ContKeys :
        if pressedKeys[key] == 1 :
            return True
    return False

def compareKeys(key1, key2) :
    """
    Returns true if the control keys are at the same state in both inputs
    """
    global ContKeys
    for k in ContKeys :
        if key1[k] != key2[k] :
            return False
    return True

def getKeyPress(kB, lastKeys, repeat=False) :
    """
    Checks of the inputs are repeated from the last input
    """
    keys = pg.key.get_pressed()
    if isKeyPressed(keys) :
        if kB == [] :
            if lastKeys is None or repeat or not compareKeys(keys, lastKeys) :
                kB.append(keys)
        else :
            if repeat or not compareKeys(keys, kB[-1]) :
                kB.append(keys)
    return kB


def play(nb) :
    Window = pg.display.set_mode((0, 0))
    lvl = Level(nb)
    if not lvl.makeLvl :
        print('error, non exising level')
        return False
    lvl.mainLogic()
    Steps = [[lvl.copyAllVars(), 0]]
    keyBuffer = []
    keys = None
    counter = 0

    lvl.drawBG(Window, counter)
    lvl.draw(Window, False)
    pg.time.wait(200)

    while True :
        if not lvl.makeLvl :
            print('error, non exising level')
            return False

        for event in pg.event.get():
        
            if event.type == QUIT :
                return False
        
        keyBuffer = getKeyPress(keyBuffer, keys, repeat=True)

        if len(keyBuffer) > 0 :
            time0 = pg.time.get_ticks()
            keys = keyBuffer.pop(0)
            turnUp = False

            ##Undo

            if keys[K_BACKSPACE] == 1 or keys[K_RCTRL] == 1:
                if len(Steps) > 1 :
                    prevStep = Steps.pop()
                    lvl.setAllVars(Steps[-1][0])
                    counter = Steps[-1][1]
                    lvl.mainLogic()

                    for kk in range(4) :
                        lvl.drawBG(Window, counter)
                        lvl.draw(Window, k=kk, prev_step=prevStep[0])
                        pg.time.wait(10)  
                    lvl.drawBG(Window, counter)
                    lvl.draw(Window, k=4)


            ##Player movement
                
            if lvl.getP() is not None and keys[K_UP] == 1 :
                turnUp = True
                lvl.setPDir('U')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and keys[K_DOWN] == 1 :
                turnUp = True
                lvl.setPDir('D')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and keys[K_RIGHT] == 1 :
                turnUp = True
                lvl.setPDir('R')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and keys[K_LEFT] == 1 :
                turnUp = True
                lvl.setPDir('L')
                lvl.push(lvl.getP(), lvl.getPDir())                


            ##Shoot bullet or Swap

            elif keys[K_SPACE] == 1 :
                lvl.PbSwap()
                lvl.mainLogic()
                turnUp = True


            ##Wait turn

            elif keys[K_RETURN] == 1 :
                turnUp = True


            ##Reset level

            elif keys[K_KP_PLUS] == 1 :
                lvl.setAllVars(Steps[0][0])
                lvl.mainLogic()
                Steps.append([lvl.copyAllVars(), 0])
                counter = 0
            

            ##Return to menu

            elif keys[K_ESCAPE] == 1 :
                return False


            #Check if the action isn't undo or reset
            if turnUp :
                counter += 1

                #Updating all the logic of the level :
                lvl.mainLogic()

                #bullet crushing and movement
                lvl.checkbCrush()
                lvl.bUpdate()

                #boxes crushed in doors
                lvl.boxCrushed()

                #Player crushed in doors
                lvl.checkPCrush()

                #Updating the undo storage
                Steps.append([lvl.copyAllVars(), counter])

                for kk in range(4) :
                    lvl.drawBG(Window, counter)
                    lvl.draw(Window, k=kk, prev_step=Steps[-2][0])
                    pg.time.wait(10)
            
            lvl.drawBG(Window, counter)
            lvl.draw(Window, k=4)

            getKeyPress(keyBuffer, keys)
            for i in range(1,4) :
                waited = False
                while pg.time.get_ticks() < time0 + i*50 :
                    waited = True
                if waited :
                    getKeyPress(keyBuffer, keys)

            #Here to avoid buffered double-inputs

            if lvl.Win() :
                return True