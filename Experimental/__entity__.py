import pygame as pg
import os

#Constants :
delta = 64
directions = ["U", "R", "D", "L"]

class entity :
    def __init__(self, coordinates, type) :
        self.x, self.y = coordinates
        self.Type = type
        self.dir = None
        if self.Type == 'P' :
            self.sprites = []
            for d in directions :
                sprite = pg.image.load(os.path.join("sprites\\player" + d + ".png"))
                self.sprites.append(pg.transform.scale(sprite, (delta, delta)))
        elif self.Type == 'b' :
            self.sprites = []
            for d in directions :
                sprite = pg.image.load(os.path.join("sprites\\bullet" + d + ".png"))
                self.sprites.append(pg.transform.scale(sprite, (delta, delta)))


    def getCoords(self) :
        return (self.x, self.y)


    def setCoords(self, coords) :
        self.x, self.y = coords
        return None


    def getDir(self) :
        return self.dir


    def setDir(self, direction) :
        self.dir = direction
        return None


    def getType(self) :
        return self.Type


    def copy(self) :
        entCopy = entity(self.getCoords(), self.getType())
        entCopy.setDir(self.getDir())
        return entCopy

    def getSprite(self) :
        for i in range(4) :
            if self.dir == directions[i] :
                return self.sprites[i]
