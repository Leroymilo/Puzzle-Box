import pygame as pg
from pygame.locals import *
pg.init()
import numpy as np
from os import listdir

from __game__ import *
from __input__ import *


delta = 32

#Functions and procedures

def updateDisplay() :
    global Window
    global H
    global W
    global bottomHUDw
    global bottomHUDh
    bottomHUDh, bottomHUDw = delta, delta*len(Elements)
    h, w = grid.shape
    H = delta*h+topHUDh+bottomHUDh
    W = max(delta*w, max(topHUDw, bottomHUDw))
    Window = pg.display.set_mode((W, H))

def changeSize() :
    nh = int(textInput('New height :'))
    nw = int(textInput('New width :'))
    global grid
    h, w = grid.shape
    ngrid = np.array([['.']*nw for _ in range(nh)])
    for x in range(min(w, nw)) :
        for y in range(min(h, nh)) :
            ngrid[y, x] = grid[y, x]
    grid = ngrid
    updateDisplay()

def loadLevel() :
    lvlnb = textInput('Level Id')
    if lvlnb is None or lvlnb == '' :
        return
    global levelnb
    levelnb = int(lvlnb)
    strn = lvlnb.rjust(3, '0')

    dir_ = "levels\\level" + strn + ".txt"
    try :
        File = open(dir_)
    except :
        return False
    Lines = File.readlines()
    File.close()
    global name
    global grid
    name = Lines[0].strip('\n')
    h = int(Lines[1].split(' ')[0])
    grid = np.array([line.strip('\n').split(' ') for line in Lines[2:h+2]])

    dir_ = "logic\\links" + strn + ".txt"
    try :
        File = open(dir_)
    except :
        return False
    Lines = File.readlines()
    File.close()
    global links
    global nodePaths
    global paths
    links, nodePaths, paths = [], [], []
    for line in Lines :
        line = line.split(' ')
        link = ((int(line[0]), int(line[1])), (int(line[2]), int(line[3])))
        links.append(link)
        paths.append(PF(link))
    return True

def getFirstDispNb() :
    used_nb = [0]+[int(name[5:8]) for name in listdir("levels")]
    global levelnb
    while levelnb in used_nb :
        levelnb += 1
    return saveLevel()

def saveLevel() :
    if levelnb == 0 :
        return saveLevelAs()
    strn = str(levelnb).rjust(3, '0')
    dir_ = "levels\\level" + strn + ".txt"
    File = open(dir_, 'w')
    h, w = grid.shape
    text = f'{name}\n{h} {w}\n' + '\n'.join([' '.join(line) for line in grid])
    File.write(text)
    File.close()
    dir_ = "logic\\links" + strn + ".txt"
    File = open(dir_, 'w')
    text = ''
    for link in links :
        (s, e) = link
        text += ' '.join((str(s[0]), str(s[1]), str(e[0]), str(e[1])))+'\n'
    File.write(text)
    File.close()

def saveLevelAs() :
    lvlnb = textInput('Level Id (0 for first disponible Id)')
    if lvlnb is None or lvlnb == '' :
        return
    global levelnb
    levelnb = int(lvlnb)
    if levelnb == 0 :
        getFirstDispNb()
    saveLevel()

def PF(link) :
    #A hard copy of what's in __logic__.py.
    #It also uses methods and functions of this script.
    h, w = grid.shape
    pgrid = np.array([['.']*w for _ in range(h)])
    for x in range(w) :
        for y in range(h) :
            if grid[y, x] in 'ID&|!T' :
                pgrid[y, x] = 'X'
    ((sx, sy), (ex, ey)) = link
    
    sGate, eGate = False, False
    if grid[sy, sx] in '&|!' :
        sy = sy-1
        sGate = True
    if grid[ey, ex] in '&|!' :
        ey = ey+1
        eGate = True

    if (sx, sy) == (ex, ey) :
        path = [(sx, sy)]
    else :
        pgrid[sy, sx] = 'A'
        pgrid[ey, ex] = 'B'
        path = pf.pathFind(pgrid)
            
    if sGate :
        path.append(link[0])
    if eGate :
        path = [link[1]] + path

    truePath = []
    nodePath = chain2nodes(path[::-1])
    nodePaths.append(nodePath)

    for jj in range(len(nodePath)-1) :
        s, e = nodePath[jj], nodePath[jj+1]
        
        if jj == 0 :
            truePath.append((s[0]*delta + delta//2, s[1]*delta + delta//2))
            truePath.append((e[0]*delta + delta//2, e[1]*delta + delta//2))
        else :
            if s[0] == e[0] :
                direction = 0
            else :
                direction = 1
            c = countOverlap(nodePaths, s, e, direction)
            offset = getOffset(c)
            truePath[-1] = addOffset(truePath[-1], offset, direction)
            truePath.append((e[0]*delta + delta//2, e[1]*delta + delta//2))
            truePath[-1] = addOffset(truePath[-1], offset, direction)
    
    return truePath

def displayTopHUD() :
    global Window
    Window.fill((180, 180, 180))
    Window.blit(TopHUD, (0, 0))
    h, w = grid.shape
    hstr, wstr = str(h).rjust(3, '0'), str(w).rjust(3, '0')
    wtxt = font.render(wstr, True, (0, 0, 0))
    Window.blit(wtxt, (444, 4))
    htxt = font.render(hstr, True, (0, 0, 0))
    Window.blit(htxt, (541, 4))

    if Connect :
        Window.blit(Cross, (114, 37))

def displayGrid() :
    global Window
    h, w = grid.shape
    x0 = (Window.get_width()-len(grid[0])*delta)//2
    y0 = topHUDh


    for x in range(w) :
        for y in range(h) :
            px, py = x0 + x*delta,  y0 + y*delta
            Window.blit(Floor, (px, py))
            for i in range(6) :
                el = Elements[i]
                if grid[y, x] == el :
                    Window.blit(Sprites[i], (px, py))
                    break
    
    Surface = pg.display.get_surface()
    for i in range(len(links)) :
        #The color of the line will depend of the state of the link
        link = links[i]
        path = paths[i]
        color = (60, 80, 255)

        sx, sy = link[0]
        ex, ey = link[1]
        
        for ii in range(len(path)-1) :
            start = (x0 + path[ii][0], y0 + path[ii][1])
            end = (x0 + path[ii+1][0], y0 + path[ii+1][1])
            pg.draw.line(Surface, color, start, end)
    
    for x in range(w) :
        for y in range(h) :
            px, py = x0 + x*delta,  y0 + y*delta
            for i in range(6, 12) :
                if grid[y, x] == Elements[i] :
                    Window.blit(Sprites[i], (px, py))
                    break

    if startLink is not None :
        px, py = x0 + startLink[0]*delta, y0 + startLink[1]*delta
        Window.blit(Select, (px, py))

def displayBottomHUD() :
    global Window
    y0 = Window.get_height()-bottomHUDh
    x0 = (Window.get_width()-len(Elements)*delta)//2
    for i in range(len(Elements)) :
        Window.blit(Floor, (x0 + i*delta, y0))
        Window.blit(Sprites[i], (x0 + i*delta, y0))
    Window.blit(Select, (x0 + tile*delta, y0))

def display() :
    displayTopHUD()
    displayGrid()
    displayBottomHUD()
    pg.display.flip()


#Importing sprites

Player = pg.transform.scale(pg.image.load(os.path.join("sprites\\playerU.png")), (delta, delta))
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
Door = pg.transform.scale(pg.image.load(os.path.join("sprites\\Door0.png")), (delta, delta))
Sprites = [Player, Floor, Wall, Grate, Win, Box, AND, OR, NO, Target, Interruptor, Door]
Elements = 'P.XxWB&|!TID'
Select = pg.transform.scale(pg.image.load(os.path.join("sprites\\Select.png")), (delta, delta))
TopHUD = pg.image.load(os.path.join("sprites\\topHUD.png"))
Cross = pg.image.load(os.path.join("sprites\\cross.png"))
font = pg.font.SysFont('system', 36)

#Setting up variables and constants

delta = 32
name = 'levelname'
grid = np.array([['.']*12 for _ in range(10)])
links = []
nodePaths = []
paths = []
topHUDw = 604
bottomHUDw = len(Elements)*delta
topHUDh = 64
bottomHUDh = delta
Continue = True
tile = 0
levelnb = 0
Connect = False
startLink = None
H, W = 0, 0
Window = pg.display.set_mode((W, H))
prevMouse = pg.mouse.get_pressed()
updateDisplay()


#Event loop

while Continue :
    for event in pg.event.get() :
        if event.type == QUIT :
            Continue = False

        #Some room for eventual hotkeys

        else :
            mouse = pg.mouse.get_pressed()
            if mouse[0] and not prevMouse[0] :
                try :
                    x, y = event.pos
                except :
                    x, y = -1, -1
                
                if y > Window.get_height() - bottomHUDh and not Connect :
                    w = len(Elements)
                    sqx = (x-(Window.get_width()-w*delta)//2)//delta
                    tile = sqx
                
                elif y > topHUDh :
                    h, w = grid.shape
                    sqx, sqy = (x-(Window.get_width()-w*delta)//2)//delta, (y-topHUDh)//delta
                    if 0 <= sqx < grid.shape[1] :
                        if Connect :
                            if startLink is None :
                                startLink = (sqx, sqy)
                            else :
                                newlink = (startLink, (sqx, sqy))
                                if newlink not in links :
                                    links.append(newlink)
                                    paths.append(PF(newlink))
                                startLink = None
                        
                        else :
                            el = Elements[tile]
                            if el in 'PW' and el in grid :
                                [[py, px]] = np.argwhere(grid==el)
                                grid[py, px] = '.'
                            grid[sqy, sqx] = el
                
                elif 0 <= y < topHUDh :
                    #First line of buttons :
                    if y <= 31 :
                        if 0 <= x <= 67 :
                            saveLevel()
                        
                        elif 71 <= x <= 178 :
                            saveLevelAs()
                            updateDisplay()
                        
                        elif 182 <= x <= 247 :
                            loaded = loadLevel()
                            if not loaded :
                                print("File not found")
                            updateDisplay()
                        
                        elif 251 <= x <= 312 :
                            saveLevel()
                            play(levelnb)
                            updateDisplay()
                        
                        elif 316 <= x <= 399 :
                            changeSize()
                        

                    else :
                        if 0 <= x <= 139 :
                            Connect = not Connect

            prevMouse = mouse

    display()

