import numpy as np
import pygame as pg
import os

from __entity__ import *
from __logic__ import *


#Constants
directions = ["U", "R", "D", "L"]
#List of levels where the player is not allowed to shoot and swap :
NoSwap =  [1, 2, 3, 4, 5, 6, 7]

#Loading sprites :
Floor = pg.transform.scale(pg.image.load(os.path.join("sprites\\Floor.png")), (delta, delta))
Wall = pg.transform.scale(pg.image.load(os.path.join("sprites\\Wall.png")), (delta, delta))
Grate = pg.transform.scale(pg.image.load(os.path.join("sprites\\grate.png")), (delta, delta))
Win = pg.transform.scale(pg.image.load(os.path.join("sprites\\Win.png")), (delta, delta))
AND = pg.transform.scale(pg.image.load(os.path.join("sprites\\AND.png")), (delta, delta))
OR = pg.transform.scale(pg.image.load(os.path.join("sprites\\OR.png")), (delta, delta))
NO = pg.transform.scale(pg.image.load(os.path.join("sprites\\NO.png")), (delta, delta))
Box = pg.transform.scale(pg.image.load(os.path.join("sprites\\Box.png")), (delta, delta))
Target = pg.transform.scale(pg.image.load(os.path.join("sprites\\Target.png")), (delta, delta))
Interruptor = pg.transform.scale(pg.image.load(os.path.join("sprites\\Interruptor.png")), (delta, delta))
Door0 = pg.transform.scale(pg.image.load(os.path.join("sprites\\Door0.png")), (delta, delta))
Door3 = pg.transform.scale(pg.image.load(os.path.join("sprites\\Door3.png")), (delta, delta))

class Level :
    def __init__(self, number) :
        self.nb = str(number)
        longnb = (3-len(self.nb))*"0" + self.nb
        self.dir = "levels\level" + longnb + ".txt"
        global delta
        delta = delta

        #Checks if there's a file for the level number asked
        try :
            File = open(self.dir)
            Text = File.read()
            File.close()
            self.makeLvl = True
        except :
            self.makeLvl = False

        if self.makeLvl :
            lines = Text.split('\n')
            self.h, self.w = tuple(map(int, lines[0].split()))
            self.grid = np.array([line.split() for line in lines[1:self.h+1]])
            self.text = lines[self.h+1:]

            self.boxes = []
            self.b = None
            self.log = logic(self.nb, self.grid)
            if self.log.makeLog :
                paths = self.log.getPaths(self.grid)
                self.cables = self.log.getTruePaths(paths, delta)
            else :
                self.cables = []

            #getting entities form the defining text :
            for x in range(self.w) :
                for y in range(self.h) :
                    if self.grid[y, x] == 'P' :
                        self.P = entity((x, y), 'P')
                        self.P.setDir('U')
                        self.grid[y, x] = '.'
                    elif self.grid[y, x] == 'B' :
                        self.boxes.append(entity((x, y), 'B'))
                        self.grid[y, x] = '.'
                    elif self.grid[y, x] == 'D' :
                        self.log.addElement(x, y, 'D')
                    elif self.grid[y, x] == 'I' :
                        self.log.addElement(x, y, 'I')
                    elif self.grid[y, x] == 'T' :
                        self.log.addElement(x, y, 'T')
                    elif self.grid[y, x] == '&' :
                        self.log.addElement(x, y, '&')
                    elif self.grid[y, x] == '|' :
                        self.log.addElement(x, y, '|')
                    elif self.grid[y, x] == '!' :
                        self.log.addElement(x, y, '!')
                    elif self.grid[y, x] == 'W' :
                        self.W = (x, y)



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
        logcopy = self.log.copyStates()
        return [Pcopy, bcopy, boxescopy, logcopy]


    def reset(self) :
        return Level(self.nb)


    def setAllVars(self, varsCopy) :
        [Pcopy, bcopy, boxescopy, logcopy] = varsCopy
        if Pcopy is not None :
            self.P = Pcopy.copy()
        else :
            self.P = None
        if bcopy is not None :
            self.b = bcopy.copy()
        else :
            self.b = None
        self.boxes = [boxescopy[ii].copy() for ii in range(len(boxescopy))]
        self.log.setStates(logcopy.copy())
        return None


    """
    PUZZLE_STUFF##############################################################################################
    Methods to test colisions, win, swap and such.
    """


    def isTile(self, x, y, types) :
        if 0 <= x < self.w and 0 <= y < self.h :
            return self.grid[y, x] in types
        return False


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
        if self.isTile(x, y, 'X') :
            return True
        elif self.isTile(x, y, 'D') :
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

        if self.isWall(px, py) or self.isTile(px, py, 'Tx') :
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
                self.resetAllT()
            else :
                x, y = self.b.getCoords()
                if  not self.isTile(x, y, 'x') :
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


    def resetAllT(self) :
        """
        Resets all the targets when a bullet is shot
        or if another target is activated.
        """
        groups = self.log.getAllCables()
        for Id in range(len(groups)) :
            x, y = groups[Id][0]
            if self.grid[y, x] == 'T' :
                self.log.setLinkState(Id, False)
        return None


    def bUpdate(self) :
        """
        Updates the position of the bullet :
        if there's a wall or a box, it reflects it;
        else it goes forward
        """
        if self.b is not None :
                    nxb, nyb = self.getNextC(self.b, self.b.getDir())
                    
                    if self.isTile(nxb, nyb, 'T') :
                        self.resetAllT()
                        for Id in self.log.getIdsEmm((nxb, nyb)) :
                            self.log.setLinkState(Id, True)
                        self.b = None
                    elif self.isBoxBlocked(nxb, nyb) or self.isWall(nxb, nyb) :
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
            if self.isBoxBlocked(x, y) or self.isWall(x, y) :
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
        for el in self.log.elements :
            x, y = el[0]
            if self.grid[y, x] in 'I!' :
                Ids = self.log.getIdsEmm((x, y))
                if self.grid[y, x] == 'I' :
                    newState = self.getIntState((x, y))
                else :
                    newState = self.getGateState((x, y))
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


    def drawBG(self, Window) :
        """
        Draws the background of the level,
        i.e. everything that won't move between steps
        """
        Surface = pg.display.get_surface()
        Window.fill((0, 0, 100))
        Ww, Wh = Window.get_size()
        x0, y0 = (Ww-self.w*delta)//2, (Wh-self.h*delta)//2

        ##Drawing walls and grates
        for i in range(self.h) :
            for j in range(self.w) :
                x, y = x0 + j*delta, y0 + i*delta
                if self.grid[i, j] == 'X' :
                    Window.blit(Wall, (x, y))
                elif self.grid[i, j] == 'x' :
                    Window.blit(Grate, (x, y))
                elif self.grid[i, j] in '.&|!' :
                    Window.blit(Floor, (x, y))
                elif self.grid[i, j] == 'W' :
                    Window.blit(Floor, (x, y))
                    Window.blit(Win, (x, y))
        
        ##Writing tips
        font = pg.font.SysFont("comicsansms", 24)
        y = y0+self.h*delta
        for line in self.text :
            tip = font.render(line, True, (255, 255, 255))
            x = (Ww - tip.get_width())//2
            Window.blit(tip, (x, y))
            y += tip.get_height()

    def draw(self, Window, k=0, prev_step=None) :
        """
        Draws everything that changes between steps
        k is the animation index, going from 0 to 3
        (4 frames of animation max),
        k = 4 is to draw the new first frame.
        """
        Surface = pg.display.get_surface()
        Ww, Wh = Window.get_size()
        x0, y0 = (Ww-self.w*delta)//2, (Wh-self.h*delta)//2
        if prev_step is None :
            k = 4

        ##Drawing lines representing connections
        groups = self.log.getAllCables()
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
                start = (x0 + path[ii][0], y0 + path[ii][1])
                end = (x0 + path[ii+1][0], y0 + path[ii+1][1])
                pg.draw.line(Surface, color, start, end)

        ##Drawing logic assets (over cables)
        for element in self.log.elements :
            (xx, yy), type_ = element
            x, y = x0+xx*delta, y0+yy*delta
            if type_ == 'I' :
                Window.blit(Interruptor, (x, y))
            elif type_ == 'D' :
                Id = self.log.getIdsRec((xx, yy))[0]
                activated = self.log.getLinkState(Id)
                if activated :
                    Window.blit(Door3, (x, y))
                else :
                    Window.blit(Door0, (x, y))
            elif type_ == '&' :
                Window.blit(AND, (x, y))
            elif type_ == '|' :
                Window.blit(OR, (x, y))
            elif type_ == '!' :
                Window.blit(NO, (x, y))
            elif type_ == 'T' :
                Window.blit(Target, (x, y))

        ##Drawing boxes
        for ibox in range(len(self.boxes)) :
            x2, y2 = self.boxes[ibox].getCoords()
            x2, y2 = x0 + delta*x2, y0 + delta*y2
            if k!=4 and ibox < len(prev_step[2]) :
                x1 ,y1 = prev_step[2][ibox].getCoords()
                x1, y1 = x0 + delta*x1, y0 + delta*y1
                dx, dy = (x2-x1)//4, (y2-y1)//4
                x, y = x1+dx*k, y1+dy*k
            else :
                x, y = x2, y2
            Window.blit(Box, (x, y))

        ##Drawing the player or help text if crushed
        if self.P is not None :
            x2, y2 = self.P.getCoords()
            x2, y2 = x0 + delta*x2, y0 + delta*y2
            if k!=4 and prev_step[0] is not None :
                x1 ,y1 = prev_step[0].getCoords()
                x1, y1 = x0 + delta*x1, y0 + delta*y1
                dx, dy = (x2-x1)//4, (y2-y1)//4
                x, y = x1+dx*k, y1+dy*k
            else :
                x, y = x2, y2
            Window.blit(self.P.getSprite(), (x, y))
        else :
            font = pg.font.SysFont("comicsansms", 20)
            losetext = font.render("You were crushed, undo (RCtrl) or restart (+)", True, (180, 180, 180))
            x = (Ww - losetext.get_width())//2
            y = y0 - losetext.get_height()
            Window.blit(losetext, (x, y))

        ##Drawing the bullet
        if self.b is not None :
            x2, y2 = self.b.getCoords()
            x2, y2 = x0 + delta*x2, y0 + delta*y2
            if k!=4 and prev_step[1] is not None :
                x1 ,y1 = prev_step[1].getCoords()
                x1, y1 = x0 + delta*x1, y0 + delta*y1
                dx, dy = (x2-x1)//4, (y2-y1)//4
                x, y = x1+dx*k, y1+dy*k
            else :
                x, y = x2, y2
            Window.blit(self.b.getSprite(), (x, y))

        pg.display.flip()
        return None