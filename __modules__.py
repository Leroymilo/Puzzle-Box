"""
Classes, functions and procedures for __main__
"""

import numpy as np
import pygame as pg
import os
from pygame.locals import *


#Constants

ẟ = 32
directions = ["U", "R", "D", "L"]

#Loading sprites :
plSprites, blSprites = [], []
for d in directions :
    blSprites.append(pg.image.load(os.path.join("sprites\\bullet" + d + ".png")))
    plSprites.append(pg.image.load(os.path.join("sprites\\player" + d + ".png")))

#Classes

class level :
    def __init__(self, directory) :
        self.dir = directory
        self.nb = int(directory[3])
        File = open('levels\\' + directory)
        Text = File.read()
        File.close()
        lines = Text.split('\n')
        self.Grid = np.array([line.split(' ') for line in lines])

        #Preparing the list for the doors & interruptors logic
        maxId = 0
        for y in range(len(self.Grid)) :
            for x in range(len(self.Grid[0])) :
                tile = self.Grid[y, x]
                if len(tile) > 1 and int(tile[1])+1 > maxId:
                    maxId = int(tile[1])+1
        logic = [[False, None] for k in range(maxId)]

        if maxId > 0 :
            #associating matching doors & interruptors
            for y in range(len(self.Grid)) :
                for x in range(len(self.Grid[0])) :
                    tile = self.Grid[y, x]
                    if len(tile) > 1 :
                        Id = int(tile[1])
                        if tile[0] == 'I' :
                            logic[Id][1] = (x, y)
                        else :
                            logic[Id].append((x, y))
        self.Logic = logic

    def getState(self, objectCoords) :
        for Id in range(len(self.Logic)) :
            if objectCoords in self.Logic[Id] :
                return self.Logic[Id][0]
    
    def setState(self, state, Id) :
        self.Logic[Id][0] = state
        return None

    def copy(self) :
        return level(self.dir)
        
class entity :
    def __init__(self, C, Type, direction=None) :
        self.C = C
        self.type = Type
        if self.type == 'P' and direction is None :
            self.dir = 'U'
        else :
            self.dir = direction

    def copy(self) :
        return entity(self.C, self.type, direction=self.dir)


#Functions and procedures

def getCoords(lvl) :
    """
    Get the coordinates of the entities and the end square from the lvl file
    """
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
    """
    Returns the coordinates of the square occupied
    by the moving entity on the next step if not blocked.
    """

    d = entity.dir
    if d is None :
        d = ents[0].dir

    x, y = entity.C

    if d == 'U' :
        return x, y-1
    elif d == 'D' :
        return x, y+1
    elif d == 'R' :
        return x+1, y
    elif d == 'L' :
        return x-1, y


def isBlocked(nC, ents) :
    """
    Check if the next coordinates of the tested entity
    are blocked by another entity.
    """
    for entity in ents :
        if entity.C == nC :
            return True
    return False

def isWall(x, y, lvl) :
    """
    Checks if the coordinates are on a wall or a closed door
    """
    if lvl.Grid[y, x] == 'X' :
        return True
    elif lvl.Grid[y, x][0] == 'D' and not lvl.getState((x, y)) :
        return True
    elif lvl.Grid[y, x][0] == 'd' and lvl.getState((x, y)) :
        return True


def changeDir(entity) :
    """
    Used for the reflection of a bullet.
    """
    directions = ['U', 'R', 'D', 'L']
    for i in range(4) :
        if entity.dir == directions[i] :
            return directions[(i+2)%4]


#Procedures

def draw(data, Window) :
    """
    Draws the level and te entities with pygame.
    """
    [lvl, ents, (xW, yW)] = data
    Surface = pg.display.get_surface()
    Window.fill((240, 240, 240))

    Rect = pg.Rect(xW*ẟ, yW*ẟ, ẟ, ẟ)
    pg.draw.rect(Surface, (0, 240, 0), Rect)
    h, w = lvl.Grid.shape
    
    ##Drawing walls, grates, interruptors and doors
    for i in range(h) :
        for j in range(w) :
            Rect = pg.Rect(j*ẟ, i*ẟ, ẟ, ẟ)
            if lvl.Grid[i, j] == 'X' :
                pg.draw.rect(Surface, (0, 0, 0), Rect)
            elif lvl.Grid[i, j] == 'x' :
                pg.draw.rect(Surface, (100, 100, 100), Rect)
            elif lvl.Grid[i, j][0] == 'I' :
                pg.draw.rect(Surface, (240, 0, 0), Rect)
            elif lvl.Grid[i, j][0] == 'D' and not lvl.getState((j, i)) :
                pg.draw.rect(Surface, (100, 0, 0), Rect)
            elif lvl.Grid[i, j][0] == 'd' and lvl.getState((j, i)) :
                pg.draw.rect(Surface, (100, 0, 0), Rect)

    ##Drawing entities (player, bullet and boxes)
    for entity in ents :
        if entity is not None :
            x, y = entity.C
            if entity.type == 'P' :
                for i in range(4) :
                    if entity.dir == directions[i] :
                        Window.blit(plSprites[i], (x*ẟ, y*ẟ))
            if entity.type == 'b' :
                for i in range(4) :
                    if entity.dir == directions[i] :
                        Window.blit(blSprites[i], (x*ẟ, y*ẟ))
            elif entity.type == 'B' :
                Rect = pg.Rect(x*ẟ+2, y*ẟ+2, ẟ-4, ẟ-4)
                pg.draw.rect(Surface, (240, 150, 0), Rect)

    pg.display.flip()
    return None

def push(entity, ents, lvl) :
    """
    Check if there's a need to push entities recursively
    or if there's a wall blocking the pushing.
    """

    px, py = getNextC(entity, ents)

    if isWall(px, py, lvl) :
        blocked = True
    elif lvl.Grid[py, px] == 'x' and entity.type in ['P', 'B'] :
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

def entitiesCopy(entities) :
    """
    Makes a deep copy of the entities list for the undo button
    """
    entC = []
    for ent in entities :
        if ent is None :
            entC.append(None)
        else :
            entC.append(ent.copy())
    return entC

def entOnInt(ents, lvl):
    """
    Checks if there are player or boxes entity on interrupters.
    If so, change the state of the interruptor to True,
    if not, change it to False
    """
    for Id in range(len(lvl.Logic)) :
        intC = lvl.Logic[Id][1]
        pushed = False
        for ent in ents :
            if ent is not None and ent.C == intC and ent.type in ['P', 'B'] :
                pushed = True
        lvl.setState(pushed, Id)
    return lvl