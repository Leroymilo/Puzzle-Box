"""
The main file with the pygame loop, calling other .py files
"""

import numpy as np
import pygame as pg
from pygame.locals import *

from __modules__ import *
from __initlvl__ import *


#General initialisation
pg.init()
clock = pg.time.Clock()
pg.key.set_repeat(500, 100)
Continue = True

#Loading the first level
curlvl, entities, wC = nLvl()

#Constants for the level
h, w = curlvl.Grid.shape
Window = pg.display.set_mode((w*ẟ, h*ẟ))

#first draw
data = [curlvl, entities, wC]
draw(data, Window)

#entities first save for the undo function
Steps = [entitiesCopy(entities)]

#Pygame loop

while Continue :
    
    for event in pg.event.get():
        
        if event.type == QUIT :
            Continue = False

        elif event.type == KEYDOWN:
            turnUp = False

            ##Player movement

            xP, yP = entities[0].C
            
            if event.key == K_UP :
                turnUp = True
                entities[0].dir = 'U'
                push(entities[0], entities, curlvl)

            elif event.key == K_DOWN :
                turnUp = True
                entities[0].dir = 'D'
                push(entities[0], entities, curlvl)
                
            elif event.key == K_RIGHT :
                turnUp = True
                entities[0].dir = 'R'
                push(entities[0], entities, curlvl)

            elif event.key == K_LEFT :
                turnUp = True
                entities[0].dir = 'L'
                push(entities[0], entities, curlvl)                

            ##Shoot bullet or Swap

            elif event.key == K_RCTRL :
                if entities[1] is None :
                    turnUp = True
                    entities[1] = entity((xP, yP), 'b', direction=entities[0].dir)
                else :
                    x, y = entities[1].C
                    if curlvl.Grid[y, x] == '.' :
                        entities[0].C, entities[1].C = entities[1].C, entities[0].C
                        entities[0].dir, entities[1].dir = entities[1].dir, entities[0].dir

            ##Wait turn

            elif event.key == K_RETURN :
                turnUp = True

            ##Reset level

            elif event.key == K_KP_PLUS :
                curlvl, entities, wC = rLvl(curlvl)
                data = [curlvl, entities, wC]
                draw(data, Window)

                #entities first save for the undo function
                Steps = [entitiesCopy(entities)]

            ##Undo

            elif event.key == K_BACKSPACE and len(Steps) > 1 :
                entities = Steps.pop(-2)
                if len(curlvl.Logic) > 0 :
                    curlvl = entOnInt(entities, curlvl)
                data = [curlvl, entities, wC]




            #Check if the action isn't undo or reset
            if turnUp :

                #Updating all the logic groups (doors and interruptors) of the level :
                if len(curlvl.Logic) > 0 :
                    curlvl = entOnInt(entities, curlvl)

                #moving and bouncing bullet
                bullet = entities[1]
                if bullet is not None :
                    nxb, nyb = getNextC(bullet, entities)

                    if isBlocked((nxb, nyb), entities) :
                        bullet.dir = changeDir(bullet)
                    elif isWall(nxb, nyb, curlvl) :
                        bullet.dir = changeDir(bullet)
                    else :
                        bullet.C = (nxb, nyb)
                
                #Saving the current step for the undo button
                Steps.append(entitiesCopy(entities))

            draw(data, Window)

            ##Test of level completion and change for next level

            if entities[0].C == wC :
                print('win')
                #Loading the next level
                nlvl = nLvl(curlvl)
                if nlvl is None :
                    Continue = False
                else :
                    curlvl, entities, wC = nlvl

                    #Constants for the new level
                    h, w = curlvl.Grid.shape
                    Window = pg.display.set_mode((w*ẟ, h*ẟ))
                    data = [curlvl, entities, wC]

                    #first draw of the new level
                    draw(data, Window)

                    #entities first save for the undo function
                    Steps = [entitiesCopy(entities)]

pg.quit()


