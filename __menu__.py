import numpy as np
import pygame as pg
from pygame.locals import *

from __game__ import *
from __level__ import *
from __logic__ import *
from __entity__ import *
from __scene__ import *
from cablesPF import *

pg.init()
pg.key.set_repeat(500, 100)

w, h = 1050, 750

#Important variables
Window = pg.display.set_mode((w, h))
Continue = True
saveId = 1
curScene = Title
page = 1
nlvl = len([name for name in os.listdir('levels') if os.path.isfile(os.path.join('levels', name))]) - 1
#Count the number of levels
pages = [np.zeros((4, 5), dtype=int) for _ in range(nlvl//20+1)]
#keep count on the completed levels of this save
Clvl = []



def loadSave(svId) :
    #Load a save from its Id (or number)
    global pages
    global Clvl
    global nlvl
    File = open("saves\\Save"+str(svId)+".txt")
    Text = File.read()
    File.close()
    Clvl = [int(lvl) for lvl in Text.split("\n")]   #list of already completed levels
    M = max(Clvl)
    for Id in range(1, nlvl+1) :
        pageId = Id//20
        line = ((Id%20)-1)//5
        col = ((Id%20-1)%5)
        if Id <= M+2 :
            if Id in Clvl :
                pages[pageId][line, col] = 3
            else :
                pages[pageId][line, col] = 2
        else :
            pages[pageId][line, col] = 1
    
    #Updating the Levels scene :
    global page
    global Scenes
    Scenes[1] = mkLvlScene(pages, page-1)

def writeSave(svId, clvl) :
    #Add the newly completed levels to the save file
    text = ''
    for lvl in clvl :
        text += str(lvl)
        text += '\n'
    text = text[:-1]
    File = open("saves\\Save"+str(svId)+".txt", 'r+')
    File.write(text)
    File.close()
    return None

def clearSave(svId) :
    #Clear the current save
    print('test')
    File = open("saves\\Save"+str(svId)+".txt", 'w')
    File.write('0')
    File.close()
    return None

#Search for which levels are already completed
loadSave(saveId)




def draw(scene:Scene, Window) :
    Window.fill((0, 0, 100))
    global saveId

    font = pg.font.SysFont("comicsansms", 20)

    if scene.getName() != 'Title' :
        text = font.render('Use escape to go back', True, (255, 255, 255))
        Window.blit(text, (0, 0))

    text = font.render('Save '+str(saveId), True, (255, 255, 255))
    Window.blit(text, (0, Window.get_height()-text.get_height()))


    if scene.getName() == 'Clear' :
        font = pg.font.SysFont("comicsansms", 40)
        text = font.render('Are you sure?', True, (255, 0, 0))
        x = (Window.get_width()-text.get_width())//2
        y = 250 - 2*text.get_height()
        Window.blit(text, (x, y))

    scene.draw(Window)

    pg.display.flip()



while Continue :
    for event in pg.event.get() :
        if event.type == MOUSEBUTTONDOWN :
            x, y = event.pos

            action = curScene.click((x, y))
            if action is not None :
                if action[0] == "change scene" :
                    nS = action[1]
                    for scene in Scenes :
                        if scene.getName() == nS :
                            curScene = scene
                
                elif action[0] == "load level" :
                    nClvl = play(action[1])
                    for lvl in nClvl :
                        if not lvl in Clvl :
                            Clvl.append(lvl)
                    writeSave(saveId, Clvl)
                    loadSave(saveId)
                    curScene = Scenes[1]
                    Window = pg.display.set_mode((w, h))
                
                elif action[0] == "next page" :
                    page = (page+1)%len(pages)
                
                elif action[0] == "prev page" :
                    page = (page-1)%len(pages)
                
                elif action[0] == "load save" :
                    saveId = action[1]
                    loadSave(saveId)
                    curScene = Scenes[2]
                
                elif action[0] == "clear" :
                    clearSave(saveId)
                    loadSave(saveId)
                    curScene = Scenes[2]
        
        elif event.type == KEYDOWN and event.key == K_ESCAPE :

            pS = curScene.prevScene()
            if pS is not None :
                for scene in Scenes :
                    if scene.getName() == pS :
                        curScene = scene


        elif event.type == QUIT :
            Continue = False
        
        draw(curScene, Window)
pg.quit