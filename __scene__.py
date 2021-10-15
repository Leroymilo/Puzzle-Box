import pygame as pg

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
        text = font.render(self.t, True, (255, 255, 255))
        while text.get_height() >= self.h and text.get_width() >= self.w and size > 0 :
            size -= 1
            font = pg.font.SysFont("comicsansms", size)
            text = font.render(self.t, True, (255, 255, 255))
        
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
Title = Scene('Title', None)

def mkLvlScene(pages, pageId) :
    global Title
    Levels = Scene('Levels', 'Title')
    if pages is not None :
        page = pages[pageId]
        w = h = 80
        dlt = 120
        x = (1050 - 4*dlt - w)//2
        y = (750 - 3*dlt - h)//2
        for line in range(4) :
            for col in range(5) :
                lvl = page[line, col]
                if lvl != 0 :
                    nb = 20*pageId+5*line+col + 1
                    if lvl == 1 :
                        clr = (50, 50, 50)
                        butt = Button((x+dlt*col, y+dlt*line), (w,h), clr, str(nb), None)
                    else :
                        if lvl == 2 :
                            clr = (0, 150, 200)
                        elif lvl == 3 :
                            clr = (0, 200, 0)
                        butt = Button((x+dlt*col, y+dlt*line), (w,h), clr, str(nb), ["load level", nb])
                    Levels.addButton(butt)
        #butt = 
    return Levels

Levels = mkLvlScene(None, None)

Settings = Scene('Settings', 'Title')
Load = Scene('Load', 'Settings')
Clear = Scene('Clear', 'Settings')


#Adding buttons to these scenes
butt = Button((300, 400), (450, 100), (0, 200, 0), 'Play', ["change scene", 'Levels'])
Title.addButton(butt)
butt = Button((300, 550), (450, 100), (0, 200, 0), 'Settings', ["change scene", 'Settings'])
Title.addButton(butt)

butt = Button((300, 250), (450, 100), (0, 200, 0), 'Load', ["change scene", 'Load'])
Settings.addButton(butt)
butt = Button((300, 400), (450, 100), (200, 50, 0), 'Clear current save', ["change scene", 'Clear'])
Settings.addButton(butt)

butt = Button((300, 175), (450, 100), (0, 200, 0), 'Save 1', ["load save", 1])
Load.addButton(butt)
butt = Button((300, 325), (450, 100), (0, 200, 0), 'Save 2', ["load save", 2])
Load.addButton(butt)
butt = Button((300, 475), (450, 100), (0, 200, 0), 'Save 3', ["load save", 3])
Load.addButton(butt)

butt = Button((300, 250), (450, 100), (200, 0, 0), 'Clear save progress', ["clear"])
Clear.addButton(butt)
butt = Button((300, 400), (450, 100), (0, 200, 0), 'Fuck go back', ["change scene", 'Settings'])
Clear.addButton(butt)

Scenes = [Title, Levels, Settings, Load, Clear]