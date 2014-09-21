import pygame
import images
import TextBox
from colors import *

class MessageBox:
    '''Horizontal bar with messages'''
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.image = images.HudMessageBackground
        self.rightimage = images.HudMessageBackgroundRight
        self.leftimage = images.HudMessageBackgroundLeft
        self.minwidth = 1.5*self.image.get_width()


    def draw(self, region):
        '''Draw the message box'''
        region = pygame.Rect(region)
        horizontaltilenumber = 0
        while horizontaltilenumber < (region.width/(self.image.get_width()-10)):
            backgroundblitposition = horizontaltilenumber*(self.image.get_width()-20)
            self.window.blit(self.image, region.move(backgroundblitposition, 0))
            horizontaltilenumber += 1
        self.window.blit(self.leftimage, region)
        self.window.blit(self.rightimage, region.move((region.width-self.image.get_width()), 0))
        TextBox.draw(self.window, "Hello, world!", region, size=18, color=BLACK, ycentered=True, beveled=False)




