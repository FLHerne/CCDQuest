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
        self.minwidth = 1.2*self.image.get_width()


    def draw(self, region, string):
        '''Draw the message box'''
        region = pygame.Rect(region)
        
        textwidth = region.height + TextBox.draw(self.window, string, region.move(0, 2), size=18, color=BLACK, ycentered=True, beveled=False, rendering=False)
        
        horizontaltilenumber = 0
        width = max(textwidth, self.minwidth)
        #region.width = width+(2*region.height)
        region.inflate_ip(width-region.width, 0)
        
        while (horizontaltilenumber+1)*(self.image.get_width()) < width:
            backgroundblitposition = horizontaltilenumber*(self.image.get_width())
            self.window.blit(self.image, region.move(backgroundblitposition, 0))
            horizontaltilenumber += 1
        self.window.blit(self.leftimage, region)
        self.window.blit(self.rightimage, region.move((width-self.rightimage.get_width()), 0))
        TextBox.draw(self.window, string, region.move(0, 2), size=18, color=BLACK, ycentered=True, beveled=False)




