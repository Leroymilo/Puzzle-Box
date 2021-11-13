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
pg.key.set_repeat(200, 200)


#reading the config files
File = open("config")
config = [data.split(' ') for data in File.read().split('\n')]
File.close()
File = open("levels\config")
lvlConfig = [[int(nb) for nb in page.split(' ')] for page in File.read().split('\n')]
File.close()

#Initialising variables and constants
Window = pg.display.set_mode((0, 0))
AddButtons(Window)
w, h = Window.get_size()
Continue = True
saveId = int(config[0][1])
curScene = Title
pageId = 0
pages = []

#Scaling the title to the screen :
title = pg.image.load(os.path.join("menu sprites\\Title.png"))
th = h//2
tw = th*title.get_width()//title.get_height()
title = pg.transform.scale(title, (tw, th))

def createPages(lvl_config, comp_levels) :
    #Creates the pages of levels in the menu
    #based on the config file and the save file.
    #0 : level does not exist
    #1 : level is locked
    #2 : level is playable but not completed
    #3 : level is completed
    nbPages = len(lvl_config)
    M = max(comp_levels) + 2
    pages = []
    for i in range(nbPages) :
        page = np.zeros((4, 5), dtype=int)
        for j in range(len(lvl_config[i])) :
            if lvl_config[i][j] in comp_levels :
                page[j//5, j%5] = 3
            elif lvl_config[i][j] <= M :
                page[j//5, j%5] = 2
            else :
                page[j//5, j%5] = 1
        pages.append(page.copy())
    return pages

def loadSave(svId) :
    #Load a save from its Id (or number)
    global pages
    global lvlConfig
    File = open("saves\\Save"+str(svId)+".txt")
    Clvl = [int(lvl) for lvl in File.read().split("\n")]  #list of already completed levels
    File.close()
    pages = createPages(lvlConfig, Clvl)
    
    #Updating the Levels scene :
    global pageId
    global Scenes
    Scenes[1] = mkLvlScene(Window, pages, lvlConfig, pageId)

def writeSave(svId, nb) :
    #Add the newly completed levels to the save file
    File = open("saves\\Save"+str(svId)+".txt")
    Clvl = [int(lvl) for lvl in File.read().split("\n")]  #list of already completed levels
    File.close()
    if nb not in Clvl :
        text = ''
        for lvl in Clvl :
            text += str(lvl)+'\n'
        text += str(nb)
        File = open("saves\\Save"+str(svId)+".txt", 'r+')
        File.write(text)
        File.close()
    return None

def clearSave(svId) :
    #Clear the current save
    File = open("saves\\Save"+str(svId)+".txt", 'w')
    File.write('0')
    File.close()
    return None

def saveConfig() :
    global config
    text = '\n'.join([' '.join(line) for line in config])
    File = open("config", 'r+')
    File.write(text)
    File.close()



#Search for which levels are already completed
loadSave(saveId)


def draw(scene:Scene, Window) :
    Window.fill((138, 208, 238))
    Ww, Wh = Window.get_size()
    global saveId

    font = pg.font.SysFont("comicsansms", 20)

    if scene.getName() != 'Title' :
        text = font.render('Use escape to go back', True, (0, 0, 0))
    else :
        x = (Ww-title.get_width())//2
        Window.blit(title, (x, 0))
        text = font.render('Use escape to quit', True, (0, 0, 0))
    Window.blit(text, (0, 0))

    text = font.render('Save '+str(saveId), True, (0, 0, 0))
    Window.blit(text, (0, Window.get_height()-text.get_height()))


    if scene.getName() == 'Clear' :
        font = pg.font.SysFont("comicsansms", 40)
        text = font.render('Are you sure?', True, (255, 0, 0))
        x = (Window.get_width()-text.get_width())//2
        y = 250 - 2*text.get_height()
        Window.blit(text, (x, y))

    scene.draw(Window)
    
    if scene.getName() == 'Levels' :
        global pageId
        global pages
        font = pg.font.SysFont("comicsansms", 20)
        text = font.render('Page '+str(pageId+1)+'/'+str(len(pages)), True, (255, 255, 255))
        Window.blit(text, ((Ww-text.get_width())//2, Wh-text.get_height()))


    pg.display.flip()



while Continue :
    for event in pg.event.get() :
        if event.type == QUIT :
            Continue = False

        elif event.type == MOUSEBUTTONDOWN :
            x, y = event.pos

            action = curScene.click((x, y))
            if action is not None :
                if action[0] == "change scene" :
                    nS = action[1]
                    for scene in Scenes :
                        if scene.getName() == nS :
                            curScene = scene

                elif action[0] == "load level" :
                    nb = action[1]
                    finished = True
                    while finished :
                        finished = play(nb, Window)
                        if finished :
                            writeSave(saveId, nb)
                        nb += 1
                    loadSave(saveId)
                    curScene = Scenes[1]
                    Window = pg.display.set_mode((w, h))
                
                elif action[0] == "next page" :
                    pageId = (pageId+1)%len(pages)
                    Scenes[1] = mkLvlScene(Window, pages, lvlConfig, pageId)
                    curScene = Scenes[1]
                
                elif action[0] == "prev page" :
                    pageId = (pageId-1)%len(pages)
                    Scenes[1] = mkLvlScene(Window, pages, lvlConfig, pageId)
                    curScene = Scenes[1]

                elif action[0] == "load save" :
                    saveId = action[1]
                    loadSave(saveId)
                    curScene = Scenes[2]
                    config[0][1] = str(saveId)
                
                elif action[0] == "clear" :
                    clearSave(saveId)
                    loadSave(saveId)
                    curScene = Scenes[2]
        
        elif event.type == KEYDOWN and event.key == K_ESCAPE :

            pS = curScene.prevScene()
            if pS is None :
                Continue = False
            else :
                for scene in Scenes :
                    if scene.getName() == pS :
                        curScene = scene
        
        draw(curScene, Window)
pg.quit
saveConfig()