import numpy as np
import pygame as pg
from pygame.locals import *


#Constants

ẟ = 16


#Classes

class lvl :
    def __init__(self, directory) :
        self.dir = directory
        self.nb = int(directory[3])
        File = open('levels\\' + directory)
        Text = File.read()
        File.close()
        lines = Text.split('\n')
        self.Grid = np.array([line.split(' ') for line in lines])
    def copy(self) :
        return lvl(self.dir)
        
class entity :
    def __init__(self, C, Type) :
        self.C = C
        self.type = Type
        if self.type == 'P':
            self.dir = 'up'
        else :
            self.dir = None


#Functions

def getCoords(lvl) :
    h, w = lvl.Grid.shape
    ents = [None, None]
    for y in range(h) :
        for x in range(w) :
            if lvl.Grid[y, x] == 'P' :
                ents[0] = entity((x, y), 'P')
                lvl.Grid[y, x] = ' '
            elif lvl.Grid[y, x] == 'B' :
                ents.append(entity((x, y), 'B'))
                lvl.Grid[y, x] = ' '
            elif lvl.Grid[y, x] == 'W' :
                wC = x, y
                lvl.Grid[y, x] = ' '
    return wC, ents

def getNextC(entity, ents) :

    d = entity.dir
    if d is None :
        d = ents[0].dir

    x, y = entity.C

    if d == 'up' :
        return x, y-1
    elif d == 'down' :
        return x, y+1
    elif d == 'right' :
        return x+1, y
    elif d == 'left' :
        return x-1, y


def isBlocked(nC, ents) :
    for entity in ents :
        if entity.C == nC :
            return True
    return False

def changeDir(entity) :
    directions = ['up', 'right', 'down', 'left']
    for i in range(4) :
        if entity.dir == directions[i] :
            return directions[(i+2)%4]


#Procedures

def draw(data) :
    [lvl, ents, Window, (xW, yW)] = data
    Surface = pg.display.get_surface()
    Window.fill((240, 240, 240))

    Rect = pg.Rect(xW*ẟ, yW*ẟ, ẟ, ẟ)
    pg.draw.rect(Surface, (0, 240, 0), Rect)
    h, w = lvl.Grid.shape
    
    for i in range(h) :
        for j in range(w) :
            Rect = pg.Rect(j*ẟ, i*ẟ, ẟ, ẟ)
            if lvl.Grid[i, j] == 'X' :
                pg.draw.rect(Surface, (0, 0, 0), Rect)
            elif lvl.Grid[i, j] == 'x' :
                pg.draw.rect(Surface, (100, 100, 100), Rect)

    for entity in ents :
        if entity is not None :
            x, y = entity.C
            Rect = pg.Rect(x*ẟ, y*ẟ, ẟ, ẟ)
            if entity.type == 'P' :
                pg.draw.rect(Surface, (0, 0, 240), Rect)
            elif entity.type == 'b' :
                pg.draw.rect(Surface, (200, 200, 0), Rect)
            elif entity.type == 'B' :
                pg.draw.rect(Surface, (240, 150, 0), Rect)

    pg.display.flip()
    return None

def push(entity, ents, lvl) :

    px, py = getNextC(entity, ents)

    if (entity.type == 'P' and lvl.Grid[py, px] in ['X', 'x']) or (entity.type in ['b', 'B'] and lvl.Grid[py, px] == 'X') :
        blocked = True

    else :
        blocked = False
        for ent in ents[1:] :
            if ent != None and ent.C == (px, py) :
                if ent.type == 'b' :
                    ent.dir = ents[0].dir
                blocked = push(ent, ents, lvl)

    if not blocked :
        entity.C = (px, py)

    if entity.type != 'P' :
        return blocked
    return None
