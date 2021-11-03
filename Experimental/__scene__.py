import pygame as pg
import numpy as np

class Button :
    def __init__(self, coords, shape, color, text, action) :
        self.x, self.y = coords
        self.w, self.h = shape
        self.c = color
        self.t = text
        self.act = action

    def draw(self, Window) :
        Surface = pg.display.get_surface()
        Rectangle = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(Surface, self.c, Rectangle)
        
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

def mkLvlScene(Window, pages, pageId) :
    #A function to map level buttons on the Levels scene.
    global Title
    Ww, Wh = Window.get_size()
    Levels = Scene('Levels', 'Title')
    if pages is not None :
        page = pages[pageId]
        w = h = 80
        dlt = 40
        Coords = buttonGrid(Window, w, h, 5, 4, dlt)
        for line in range(4) :
            for col in range(5) :
                lvl = page[line, col]
                C = Coords[line, col]
                if lvl != 0 :
                    nb = 20*pageId + 5*line+col + 1
                    if lvl == 1 :
                        clr = (50, 50, 50)
                        butt = Button(C, (w, h), clr, str(nb), None)
                    else :
                        if lvl == 2 :
                            clr = (0, 150, 200)
                        elif lvl == 3 :
                            clr = (0, 200, 0)
                        butt = Button(C, (w, h), clr, str(nb), ["load level", nb])
                    Levels.addButton(butt)

        x0 = (Ww-(80+40)*5+40)//2
        x1, x2 = x0-20-45, Ww-x0+20
        y = Coords[0, 0][1] + 175
        butt = Button((x1, y), (45, 90), (138, 208, 238), '', ["prev page"])
        Levels.addButton(butt)
        butt = Button((x2, y), (45, 90), (138, 208, 238), '', ["next page"])
        Levels.addButton(butt)

    return Levels

Title = Scene('Title', None)
Settings = Scene('Settings', 'Title')
Load = Scene('Load', 'Settings')
Clear = Scene('Clear', 'Settings')


#Adding buttons to these scenes
def AddButtons(Window) :
    global Title
    global Settings
    global Load
    global Clear
    
    C = buttonGrid(Window, 450, 100, 1, 4, 50)
    butt = Button(C[2, 0], (450, 100), (213, 219, 90), 'Play', ["change scene", 'Levels'])
    Title.addButton(butt)
    butt = Button(C[3, 0], (450, 100), (213, 219, 90), 'Settings', ["change scene", 'Settings'])
    Title.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 2, 50)
    butt = Button(C[0, 0], (450, 100), (213, 219, 90), 'Load', ["change scene", 'Load'])
    Settings.addButton(butt)
    butt = Button(C[1, 0], (450, 100), (200, 50, 0), 'Clear current save', ["change scene", 'Clear'])
    Settings.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 3, 50)
    butt = Button(C[0, 0], (450, 100), (213, 219, 90), 'Save 1', ["load save", 1])
    Load.addButton(butt)
    butt = Button(C[1, 0], (450, 100), (213, 219, 90), 'Save 2', ["load save", 2])
    Load.addButton(butt)
    butt = Button(C[2, 0], (450, 100), (213, 219, 90), 'Save 3', ["load save", 3])
    Load.addButton(butt)

    C = buttonGrid(Window, 450, 100, 1, 2, 50)
    butt = Button(C[0, 0], (450, 100), (200, 0, 0), 'Clear save progress', ["clear"])
    Clear.addButton(butt)
    butt = Button(C[1, 0], (450, 100), (213, 219, 90), 'Fuck go back', ["change scene", 'Settings'])
    Clear.addButton(butt)

Scenes = [Title, None, Settings, Load, Clear]