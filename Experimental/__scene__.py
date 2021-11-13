import pygame as pg
import numpy as np
import os

#Importing button sprites :
prev_page = pg.image.load(os.path.join("menu sprites\\prev_page.png"))
next_page = pg.image.load(os.path.join("menu sprites\\next_page.png"))
buttons = [pg.image.load(os.path.join("menu sprites\\button"+str(i)+".png")) for i in range(2)]
lvlbuttons = [pg.image.load(os.path.join("menu sprites\\lvl"+str(i)+".png")) for i in range(1, 4)]

class Button :
    def __init__(self, coords, sprite, text, action) :
        self.x, self.y = coords
        self.sp = sprite
        self.w, self.h = self.sp.get_width(), self.sp.get_height()
        self.t = text
        self.act = action

    def draw(self, Window) :
        Window.blit(self.sp, (self.x, self.y))
        
        if self.t is not None :
            size = 32
            font = pg.font.SysFont("comicsansms", size)
            text = font.render(self.t, True, (0, 0, 0))
            while text.get_height() >= self.h and text.get_width() >= self.w and size > 0 :
                size -= 1
                font = pg.font.SysFont("comicsansms", size)
                text = font.render(self.t, True, (0, 0, 0))
            
            x = self.x + (self.w-text.get_width())//2
            y = self.y + (self.h-text.get_height())//2
            Window.blit(text, (x ,y))

    def click(self, C) :
        x, y = C
        if self.x <= x <= self.x+self.w and self.y <= y <= self.y+self.h :
            return self.act
        return None

class Scene :
    def __init__(self, name, parent) :
        self.n = name
        self.p = parent
        self.buttons = []

    def addButton(self, button) :
        self.buttons.append(button)
        return None

    def getName(self) :
        return self.n

    def prevScene(self) :
        return self.p

    def click(self, C) :
        for b in self.buttons :
            act = b.click(C)
            if act is not None :
                return act
    
    def draw(self, Window) :
        for b in self.buttons :
            b.draw(Window)
        return None

#Predifined scenes for the menu :

def buttonGrid(Window, butw, buth, butnbx, butnby, delta) :
    #This function gives the coordinates of each button centered in the screen.
    Ww, Wh = Window.get_size()
    x0 = (Ww-(butw+delta)*butnbx+delta)//2
    y0 = (Wh-(buth+delta)*butnby+delta)//2
    return np.array([[(x0 + j*(butw+delta), y0 + i*(buth+delta)) for j in range(butnbx)] for i in range(butnby)])

def mkLvlScene(Window, pages, lvl_config, pageId) :
    #A function to map level buttons on the Levels scene.
    global Title
    Ww, Wh = Window.get_size()
    Levels = Scene('Levels', 'Title')
    if pages is not None :
        page = pages[pageId]
        w = h = 80
        dlt = 40
        Coords = buttonGrid(Window, w, h, 5, 4, dlt)
        for i in range(len(lvl_config[pageId])) :
            nb = lvl_config[pageId][i]
            line, col = i//5, i%5
            lvlState = page[line, col]
            C = Coords[line, col]
            if lvlState != 0 :
                if lvlState == 1 :
                    butt = Button(C, lvlbuttons[0], str(nb), None)
                else :
                    butt = Button(C, lvlbuttons[lvlState-1], str(nb), ["load level", nb])
                Levels.addButton(butt)

        x0 = (Ww-(80+40)*5+40)//2
        x1, x2 = x0-20-45, Ww-x0+20
        y = Coords[0, 0][1] + 175
        butt = Button((x1, y), prev_page, '', ["prev page"])
        Levels.addButton(butt)
        butt = Button((x2, y), next_page, '', ["next page"])
        Levels.addButton(butt)

    return Levels


#Initialising all the scenes
Title = Scene('Title', None)
Settings = Scene('Settings', 'Title')
Load = Scene('Load', 'Settings')
Clear = Scene('Clear', 'Settings')


#Adding buttons to these scenes based on the size of the screen
def AddButtons(Window) :
    global Title
    global Settings
    global Load
    global Clear
    
    C = buttonGrid(Window, 450, 100, 1, 4, 50)
    butt = Button(C[2, 0], buttons[0], 'Play', ["change scene", 'Levels'])
    Title.addButton(butt)
    butt = Button(C[3, 0], buttons[0], 'Settings', ["change scene", 'Settings'])
    Title.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 2, 50)
    butt = Button(C[0, 0], buttons[0], 'Load save', ["change scene", 'Load'])
    Settings.addButton(butt)
    butt = Button(C[1, 0], buttons[1], 'Clear save', ["change scene", 'Clear'])
    Settings.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 3, 50)
    butt = Button(C[0, 0], buttons[0], 'Save 1', ["load save", 1])
    Load.addButton(butt)
    butt = Button(C[1, 0], buttons[0], 'Save 2', ["load save", 2])
    Load.addButton(butt)
    butt = Button(C[2, 0], buttons[0], 'Save 3', ["load save", 3])
    Load.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 2, 50)
    butt = Button(C[0, 0], buttons[1], 'Clear save progress', ["clear"])
    Clear.addButton(butt)
    butt = Button(C[1, 0], buttons[0], 'Nevermind', ["change scene", 'Settings'])
    Clear.addButton(butt)

Scenes = [Title, None, Settings, Load, Clear]