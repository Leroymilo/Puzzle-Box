import pygame as pg
from pygame.locals import *

from __level__ import *

pg.init()
pg.key.set_repeat(500, 100)

delta = 32
lvl = Level(1)
Steps = [lvl.copyAllVars()]

w, h = lvl.getShape()
Window = pg.display.set_mode((delta*w, delta*h))

lvl.draw(Window)

Continue = True

while Continue :
    for event in pg.event.get() :
        turnUp = False
    
        if event.type == QUIT :
            Continue = False

        elif event.type == KEYDOWN:


            ##Undo

            if event.key == K_BACKSPACE or event.key == K_RCTRL:
                if len(Steps) > 1 :
                    Steps.pop()
                    lvl.setAllVars(Steps[-1])
                    lvl.mainLogic()


            ##Player movement
            if lvl.getP() is not None :
                xP, yP = lvl.getPCoords()
                
            if lvl.getP() is not None and event.key == K_UP :
                turnUp = True
                lvl.setPDir('U')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and event.key == K_DOWN :
                turnUp = True
                lvl.setPDir('D')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and event.key == K_RIGHT :
                turnUp = True
                lvl.setPDir('R')
                lvl.push(lvl.getP(), lvl.getPDir())

            elif lvl.getP() is not None and event.key == K_LEFT :
                turnUp = True
                lvl.setPDir('L')
                lvl.push(lvl.getP(), lvl.getPDir())                


            ##Shoot bullet or Swap

            elif event.key == K_SPACE :
                lvl.PbSwap()
                lvl.mainLogic()
                turnUp = True


            ##Wait turn

            elif event.key == K_RETURN :
                turnUp = True


            ##Reset level

            elif event.key == K_KP_PLUS :
                lvl.setAllVars(Steps[0])
                lvl.mainLogic()
                Steps.append(lvl.copyAllVars())


            #Check if the action isn't undo or reset
            if turnUp :

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
                Steps.append(lvl.copyAllVars())
            
            lvl.draw(Window)

            if lvl.Win() :
                print('win')
                lvl = lvl.nextlevel()
                if lvl is None :
                    Continue = False
                else :
                    #Resize the window and draws
                    lvl.mainLogic()
                    w, h = lvl.getShape()
                    Window = pg.display.set_mode((delta*w, delta*h))
                    lvl.draw(Window)
                    #Resets the undo storage :
                    Steps = [lvl.copyAllVars()]


pg.quit()