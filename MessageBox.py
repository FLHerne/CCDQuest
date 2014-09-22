import pygame
import images
from TextBox import TextBox
from colors import *

class MessageBox:
    '''Horizontal bar with messages'''
    def __init__(self, window):
        self.window = window
        self.textbox = TextBox(20, BLACK, False)

    def draw(self, region, string):
        '''Draw the message box'''
        region = pygame.Rect(region)

        textsurface = self.textbox.draw(string, region, (True, True))
        MARGINX = 8
        MARGINY = 3
        boxregion = textsurface.get_rect(center=region.center).inflate(2*MARGINX, 2*MARGINY).clip(region)

        imagewidth = images.HudMessageBackground.get_width()
        horiztileoffset = 0
        while horiztileoffset+imagewidth < boxregion.width:
            self.window.blit(images.HudMessageBackground, boxregion.move(horiztileoffset, 0))
            horiztileoffset += imagewidth
        self.window.blit(images.HudMessageBackgroundLeft, boxregion)
        self.window.blit(images.HudMessageBackgroundRight, boxregion.move(-images.HudMessageBackgroundRight.get_width(), 0).topright)
        self.window.blit(textsurface, boxregion.move(MARGINX, MARGINY))
