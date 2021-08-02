import numpy as np
import pygame as pg
from pygame.locals import *

from __modules__ import *
from __initlvl__ import *


#General initialisation
pg.init()
clock = pg.time.Clock()
pg.key.set_repeat(100, 100)
Continue = True

#Loading the first level
curlvl, entities, wC = nLvl()

#Constants for the level
h, w = curlvl.Grid.shape
Window = pg.display.set_mode((w*ẟ, h*ẟ))

#first draw
data = [curlvl, entities, Window, wC]
draw(data)


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
                entities[0].dir = 'up'
                push(entities[0], entities, curlvl)

            elif event.key == K_DOWN :
                turnUp = True
                entities[0].dir = 'down'
                push(entities[0], entities, curlvl)
                
            elif event.key == K_RIGHT :
                turnUp = True
                entities[0].dir = 'right'
                push(entities[0], entities, curlvl)

            elif event.key == K_LEFT :
                turnUp = True
                entities[0].dir = 'left'
                push(entities[0], entities, curlvl)                

            elif event.key == K_SPACE :
                if entities[1] is None :
                    turnUp = True
                    entities[1] = entity((xP, yP), 'b')
                    entities[1].dir = entities[0].dir
                else :
                    entities[0].C, entities[1].C = entities[1].C, entities[0].C
                    entities[0].dir, entities[1].dir = entities[1].dir, entities[0].dir

            elif event.key == K_RSHIFT :
                turnUp = True

            elif event.key == K_RETURN :
                curlvl, entities, wC = rLvl(curlvl)
                data = [curlvl, entities, Window, wC]
                draw(data)

            elif event.key == K_BACKSPACE :
                None

            #Check if the action isn't rewind or reset
            if turnUp :

                #moving and bouncing bullet
                bullet = entities[1]
                if bullet is not None :
                    nxb, nyb = getNextC(bullet, entities)

                    if curlvl.Grid[nyb, nxb] in ['X'] or isBlocked((nxb, nyb), entities) :
                        bullet.dir = changeDir(bullet)
                        
                    else :
                        bullet.C = (nxb, nyb)
                        
            draw(data)
                
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
                    data = [curlvl, entities, Window, wC]

                    #first draw of the new level
                    pg.time.wait(500)
                    draw(data)

pg.quit()
                
            
