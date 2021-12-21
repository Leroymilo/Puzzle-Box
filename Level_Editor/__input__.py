# import sys module
import pygame as pg
import sys

def textInput(message='') :
    pg.init()
    clock = pg.time.Clock()
    fontMsg = pg.font.SysFont('system', 50)
    fontTxt = pg.font.SysFont('system', 60)
    text = '000'
    Msg = fontMsg.render(message, True, (0, 0, 0))
    Txt = fontTxt.render(text, True, (0, 0, 0))
    W = max(Msg.get_width(), Txt.get_width())
    H = Msg.get_height() + Txt.get_height()
    Rect = pg.Rect(0, Msg.get_height(), Txt.get_width(), Txt.get_height())
    Window = pg.display.set_mode((W, H))
    Window.fill((180, 180, 180))
    Window.blit(Msg, (0, 0))
    text = ''

    while True:
        for event in pg.event.get() :
    
        # if user types QUIT then the screen will close
            if event.type == pg.QUIT :
                return
    
            if event.type == pg.KEYDOWN :
                
                if event.key == pg.K_RETURN :

                    return text
                
                if event.key == pg.K_ESCAPE :

                    return

                elif event.key == pg.K_BACKSPACE :
    
                    text = text[:-1]

                elif len(text) < 3 :
                    char = event.unicode
                    if char in '0123456789' :
                        text += char
        
        

        pg.draw.rect(Window, (130, 130, 130), Rect)
        textSurf = fontTxt.render(text, True, (0, 0, 0))

        Window.blit(textSurf, (0, Msg.get_height()))

        pg.display.flip()

        clock.tick(60)