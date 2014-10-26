import pygame
import hudimages
from TextBox import TextBox
from colors import *

class MessageBox:
    '''Horizontal bar with messages'''
    def __init__(self, window, mgolist):
        self.window = window
        self.textbox = TextBox(20, BLACK, False)
        self.string = None
        self.mgolist = mgolist

    def draw(self, region):
        '''Draw the message box'''
        if self.string != None:
            region = pygame.Rect(region)

            textsurface = self.textbox.draw(self.string, region, (True, True))
            MARGINX = 8
            MARGINY = 3
            boxregion = textsurface.get_rect(center=region.center).inflate(2*MARGINX, 2*MARGINY).clip(region)

            imagewidth = hudimages.MessageBackground.get_width()
            horiztileoffset = 0
            while horiztileoffset+imagewidth < boxregion.width:
                self.window.blit(hudimages.MessageBackground, boxregion.move(horiztileoffset, 0))
                horiztileoffset += imagewidth
            self.window.blit(hudimages.MessageBackgroundLeft, boxregion)
            self.window.blit(hudimages.MessageBackgroundRight, boxregion.move(-hudimages.MessageBackgroundRight.get_width(), 0).topright)
            self.window.blit(textsurface, boxregion.move(MARGINX, MARGINY))

    def update(self):
        highestpriority = 0
        highestprioritymgo = None
        if len(self.mgolist) > 0:
            for mgo in self.mgolist:
                if mgo.message[1] > highestpriority:
                    highestpriority = mgo.message[1]
                    highestprioritymgo = mgo
            if highestprioritymgo != None and highestprioritymgo.message[0] != None:
                self.string = highestprioritymgo.message[0]
                highestprioritymgo.mdnotify()
        else:
            self.string = None