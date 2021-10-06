import numpy as np
import pygame as pg
import os

from __entity__ import *
from __logic__ import *


#Constants

directions = ["U", "R", "D", "L"]
#List of levels where the player is not allowed to swap :
NoSwap =  [1, 2, 3, 4, 5, 6, 7, 8]

#Loading sprites :
plSprites, blSprites = [], []
for d in directions :
    blSprites.append(pg.image.load(os.path.join("sprites\\bullet" + d + ".png")))
    plSprites.append(pg.image.load(os.path.join("sprites\\player" + d + ".png")))
AND = pg.image.load(os.path.join("sprites\\AND.png"))
OR = pg.image.load(os.path.join("sprites\\OR.png"))
NO = pg.image.load(os.path.join("sprites\\NO.png"))
Box = pg.image.load(os.path.join("sprites\\Box.png"))


class Level :
    def __init__(self, number) :
        self.nb = str(number)
        longnb = (3-len(self.nb))*"0" + self.nb
        self.dir = "levels\level" + longnb + ".txt"
        self.delta = 32


        #Checks if there's a file for the level number asked
        try :
            File = open(self.dir)
            Text = File.read()
            File.close()
            self.makeLvl = True
        except :
            print(self.dir + " not found")
            self.makeLvl = False

        if self.makeLvl :
            self.grid = np.array([line.split(' ') for line in Text.split('\n')])

            self.h, self.w = self.grid.shape
            self.boxes = []
            self.b = None
            self.log = logic(self.nb, self.grid)
            if self.log.makeLog :
                paths = self.log.getPaths(self.grid)
                self.cables = self.log.getTruePaths(paths, self.delta)
            else :
                self.cables = []

            #getting entities form the defining text :
            for x in range(self.w) :
                for y in range(self.h) :
                    if self.grid[y, x] == 'P' :
                        self.P = entity((x, y), 'P')
                        self.P.setDir('U')
                        self.grid[y, x] == '.'
                    if self.grid[y, x] == 'B' :
                        self.boxes.append(entity((x, y), 'B'))
                        self.grid[y, x] == '.'
                    if self.grid[y, x] == 'W' :
                        self.W = (x, y)
                        self.grid[y, x] == '.'


    """
    GETTERS&SETTERS###########################################################################################
    Methods to get and set the level's attribute from the outside.
    """


    def getP(self) :
        return self.P


    def getPCoords(self) :
        return self.P.getCoords()


    def getPDir(self) :
        return self.P.getDir()


    def setPDir(self, direction) :
        self.P.setDir(direction)
        return None


    def getShape(self) :
        return self.w, self.h


    """
    META######################################################################################################
    Functions acting about the whole level object
    """


    def copyAllVars(self) :
        if self.P is not None :
            Pcopy = self.P.copy()
        else :
            Pcopy = None
        if self.b is not None :
            bcopy = self.b.copy()
        else :
            bcopy = None
        boxescopy = [self.boxes[ii].copy() for ii in range(len(self.boxes))]
        return [Pcopy, bcopy, boxescopy]


    def reset(self) :
        return Level(self.nb)


    def nextlevel(self) :
        nlvl = Level(int(self.nb)+1)
        if nlvl.makeLvl :
            return nlvl
        return None


    def setAllVars(self, varsCopy) :
        [Pcopy, bcopy, boxescopy] = varsCopy
        if Pcopy is not None :
            self.P = Pcopy.copy()
        else :
            self.P = None
        if bcopy is not None :
            self.b = bcopy.copy()
        else :
            self.b = None
        self.boxes = [boxescopy[ii].copy() for ii in range(len(boxescopy))]
        return None


    """
    PUZZLE_STUFF##############################################################################################
    Methods to test colisions, win, swap and such.
    """


    def getNextC(self, ent:entity, d) :
        """
        Returns the coordinates of the square occupied
        by the moving entity on the next step if not blocked.
        "d" (the direction) has to be stated.
        """

        x, y = ent.getCoords()

        if d == 'U' :
            return x, y-1
        elif d == 'D' :
            return x, y+1
        elif d == 'R' :
            return x+1, y
        elif d == 'L' :
            return x-1, y


    def isWall(self, x, y) :
        """
        Checks if the coordinates are on a wall or a closed door
        """
        if self.grid[y, x] == 'X' :
            return True
        elif self.grid[y, x] == 'D' :
            doorState = not self.log.getLinkState(self.log.getIdsRec((x, y))[0])
            return doorState
        return False


    def push(self, subject:entity, direction) :
        """
        Check if there's a need to push entities recursively
        or if there's a wall blocking the pushing.
        'subject' is the entity that might push,
        direction has to be stated.
        """

        px, py = self.getNextC(subject, direction)

        if self.isWall(px, py) or self.grid[py, px] == 'x' :
            blocked = True
        else :
            blocked = False
            for box in self.boxes :
                if box.getCoords() == (px, py) :
                    blocked = self.push(box, direction)

        if not blocked :
            subject.setCoords((px, py))

        if subject.getType() != 'P' :
            return blocked
        return None


    def Win(self) :
        if self.P is not None :
            return (self.P.getCoords() == self.W)
        else :
            return False


    def PbSwap(self) :
        if int(self.nb) not in NoSwap and self.P is not None :
            if self.b is None :
                turnUp = True
                self.b = entity(self.P.getCoords(), 'b')
                self.b.setDir(self.P.getDir())
            else :
                x, y = self.b.getCoords()
                if self.grid[y, x] != 'x' :
                    self.b.setCoords(self.P.getCoords())
                    self.P.setCoords((x, y))
                    PDir = self.P.getDir()
                    self.P.setDir(self.b.getDir())
                    self.b.setDir(PDir)


    def isBoxBlocked(self, nx, ny) :
        """
        Checks if there's a box at nCoords
        """
        for box in self.boxes :
            if box.getCoords() == (nx ,ny) :
                return True
        return False


    def changeDir(self, ent:entity) :
        """
        Reverses the direction of ent
        """
        d = ent.getDir()
        for k in range(4) :
            if d == directions[k] :
                ent.setDir(directions[k-2])
        return None


    def bUpdate(self) :
        """
        Updates the position of the bullet :
        if there's a wall or a box, it reflects it;
        else it goes forward
        """
        if self.b is not None :
                    nxb, nyb = self.getNextC(self.b, self.b.getDir())

                    if self.isBoxBlocked(nxb, nyb) or self.isWall(nxb, nyb) :
                        self.changeDir(self.b)
                    else :
                        self.b.setCoords((nxb, nyb))
        return None


    def checkbCrush(self) :
        """
        Checks if the bullet has been crushed between boxes and walls.
        """
        if self.b is not None :
            x, y = self.b.getCoords()
            for box in self.boxes :
                if box.getCoords() == (x, y) :
                    self.b = None
            if self.isWall(x, y) :
                self.b = None
        return None

    def checkPCrush(self) :
        """
        Checks if the player is crushed by a door or by the bullet.
        """
        if self.P is not None :
            x, y = self.P.getCoords()
            if self.isWall(x, y) :
                self.P = None
            elif self.b is not None and self.P.getCoords() == self.b.getCoords() :
                self.P = None
                self.b = None



    def boxCrushed(self) :
        """
        Checks if boxes are getting crushed by closing doors,
        deletes them if so.
        """
        crushed = []
        for k in range(len(self.boxes)) :
            x, y = self.boxes[k].getCoords()
            if self.isWall(x, y) :
                crushed += [k-len(crushed)]
        for i in crushed :
            self.boxes.pop(i)


    """
    LOGIC#####################################################################################################
    All the functions to handle interruptors, targets(todo), logic gates and doors.
    Only mainLogic() is to be called in __main__.
    """


    def getIntState(self, Coords) :
        """
        Check if there's any box or the player on the interruptor.
        The state is True if the interruptor is pressed
        """
        state = False
        for box in self.boxes :
            if box.getCoords() == Coords :
                state = True
        if not state and self.P is not None :
            state = (self.P.getCoords() == Coords)
        return state


    def updateLogic(self, Ids, newState) :
        #Update the state of a group
        csi = []
        for Id in Ids :
            oldState = self.log.getLinkState(Id)
            if newState != oldState :
                self.log.setLinkState(Id, newState)
                csi.append(Id)
            else :
                #The group needs to be updated
                #if the receiver is a not gate.
                Rx, Ry = self.log.getLinkRec(Id)
                if self.grid[Ry, Rx] == '!' :
                    csi.append(Id)
        return csi


    def getGateState(self, Coords) :
        """
        Returns the state of the gate at "Coords"
        """
        x, y = Coords
            
        if self.grid[y, x] == '&' :
            #AND gate

            Ids = self.log.getIdsRec(Coords)
            if len(Ids) <= 1 :
                print("not enough inputs for AND gate in level " + str(self.nb) + " at " + str(Coords))

            if len(Ids) == 0 :
                state = False
            else :
                state = True
                for Id in Ids :
                    if not self.log.getLinkState(Id) :
                        state = False

            return state
                    
                
        if self.grid[y, x] == '|' :
            #OR gate

            Ids = self.log.getIdsRec(Coords)
            if len(Ids) <= 1 :
                print("not enough inputs for OR gate in level " + str(self.nb) + " at " + str(Coords))

            state = False
            for Id in Ids :
                if self.log.getLinkState(Id) :
                    state = True
            
            return state
        
        if self.grid[y, x] == '!' :
            #NOT gate

            Ids = self.log.getIdsRec(Coords)
            if len(Ids) == 0 :
                print("no input for NOT gate in level " + str(self.nb) + " at " + str(Coords))
                print("returning False")
                return False

            elif len(Ids) > 1 :
                print("too many inputs for NOT gate in level " + str(self.nb) + " at " + str(Coords))
                print("returning False")
                return False

            else :
                return (not self.log.getLinkState(Ids[0]))


    def mainLogic(self) :
        """
        CSI stands for Changed States Ids,
        it's the list of link's Ids that have been their state changed
        CSI is in the arguments for Targets(todo) logic
        """
        CSI = []
        for x in range(self.w) :
            for y in range(self.h) :
                Coords = x, y
                if self.grid[y, x] == 'I' :
                    Ids = self.log.getIdsEmm(Coords)
                    newState = self.getIntState(Coords)
                    CSI += self.updateLogic(Ids, newState)
        gatesInCSI = True
        while gatesInCSI :
            #loop while there are updated gates in the links' Ids
            gatesInCSI = False
            for Id in CSI :
                x, y = self.log.getLinkRec(Id)
                if self.grid[y, x] in ['&', '|', '!'] :
                    gatesInCSI = True
                    newState = self.getGateState((x, y))
                    outputIds = self.log.getIdsEmm((x, y))
                    CSI.remove(Id)
                    CSI += self.updateLogic(outputIds, newState)
        #At the end of this loop, there should only be door receivers in the CSI links.
        
        return None


    """
    DRAW######################################################################################################
    Function for drawing the level
    """


    def draw(self, Window) :
        """
        Draws the whole level using pygame
        """
        Surface = pg.display.get_surface()
        Window.fill((240, 240, 240))

        Rect = pg.Rect(self.W[0]*self.delta, self.W[1]*self.delta, self.delta, self.delta)
        pg.draw.rect(Surface, (0, 240, 0), Rect)

        ##Drawing walls, grates, interruptors, doors and logic gates
        for i in range(self.h) :
            for j in range(self.w) :
                Rect = pg.Rect(j*self.delta, i*self.delta, self.delta, self.delta)
                if self.grid[i, j] == 'X' :
                    pg.draw.rect(Surface, (0, 0, 0), Rect)
                elif self.grid[i, j] == 'x' :
                    pg.draw.rect(Surface, (100, 100, 100), Rect)
                elif self.grid[i, j][0] == 'I' :
                    pg.draw.rect(Surface, (240, 0, 0), Rect)
                elif self.grid[i, j][0] == 'D' :
                    Id = self.log.getIdsRec((j, i))[0]
                    activated = self.log.getLinkState(Id)
                    if activated :
                        pg.draw.rect(Surface, (255, 170, 170), Rect)
                    else :
                        pg.draw.rect(Surface, (180, 0, 0), Rect)
                elif self.grid[i, j][0] == '&' :
                    Window.blit(AND, (j*self.delta, i*self.delta))
                elif self.grid[i, j][0] == '|' :
                    Window.blit(OR, (j*self.delta, i*self.delta))
                elif self.grid[i, j][0] == '!' :
                    Window.blit(NO, (j*self.delta, i*self.delta))

        ##Drawing lines representing connections
        groups = self.log.getAll()
        for id in range(len(groups)) :
            #The color of the line will depend of the state of the link
            link = groups[id]
            path = self.cables[id]
            if link[2] :
                color = (255, 130, 40)
            else :
                color = (60, 80, 255)

            sx, sy = link[0]
            ex, ey = link[1]
            
            for ii in range(len(path)-1) :
                start, end = path[ii], path[ii+1]
                pg.draw.line(Surface, color, start, end)

        ##Drawing boxes
        for box in self.boxes :
            x, y = box.getCoords()
            Window.blit(Box, (x*self.delta, y*self.delta))

        ##Drawing the player or help text if crushed
        if self.P is not None :
            x, y = self.P.getCoords()
            for i in range(4) :
                if self.P.getDir() == directions[i] :
                    Window.blit(plSprites[i], (x*self.delta, y*self.delta))
        else :

            #Render text (to fit the screen)
            pg.init()
            size = 24
            font = pg.font.SysFont("comicsansms", size)
            losetext = font.render("You were crushed, undo (RCtrl) or restart (+)", True, (180, 180, 180))
            while losetext.get_width() > self.w*self.delta and size > 8 :
                size -= 2
                font = pg.font.SysFont("comicsansms", size)
                losetext = font.render("You were crushed, undo (RCtrl) or restart (+)", True, (180, 180, 180))

            losetext = font.render("You were crushed, undo (RCtrl) or restart (+)", True, (180, 180, 180))
            x = (self.w*self.delta - losetext.get_width())//2
            Window.blit(losetext, (x, 0))

        ##Drawing the bullet
        if self.b is not None :
            x, y = self.b.getCoords()
            for i in range(4) :
                if self.b.getDir() == directions[i] :
                    Window.blit(blSprites[i], (x*self.delta, y*self.delta))

        pg.display.flip()
        return None