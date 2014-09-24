import pygame
from colors import *

class TextBox:
    '''Render text with given size/font/colors'''
    def __init__(self, size, color, beveled=True, font="./fonts/MorrisRomanBlack.ttf"):
        '''Set instance variables, calculate beveling colors'''
        self.font = pygame.font.Font(font, size)
        self.beveled = beveled
        self.maincolor = pygame.Color(*color).correct_gamma(1)
        self.darkcolor = BLACK #FIXME
        self.lightcolor = self.maincolor.correct_gamma(8)

    def draw(self, string, region, centered=(True, True), surface=None):
        '''Draw text to surface, or return text on a new surface'''
        textsize = self.font.size(string)
        returnsurface = False
        if surface == None:
            surface = pygame.Surface((textsize[0]+2, textsize[1]+2), pygame.SRCALPHA, 32)
            region = region.copy()
            region.topleft = (0, 0)
            offset = [1, 1]
            returnsurface = True
        else:
            offset = [region.left+1, region.top+1]
            for axis in [0, 1]:
                if centered[axis]:
                    offset[axis] += int(region.size[axis]/2 - textsize[axis]/2)
                elif axis == 1:
                    offset[axis] = region.bottom-textsize[1]-1
        for (xbeveloffset, ybeveloffset, color) in ((1, 1, self.darkcolor), (1, -1, self.lightcolor), (-1, 1, self.darkcolor), (-1, -1, self.lightcolor), (0, 0, self.maincolor)) if self.beveled else ((0, 0, self.maincolor),):
            textbitmap = self.font.render(string, True, color)
            surface.blit(textbitmap, (offset[0]+xbeveloffset, offset[1]+ybeveloffset))
        if returnsurface:
            return surface
