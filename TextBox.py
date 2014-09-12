import pygame
from colors import *

defaultsize = 12
defaultcolor = WHITE
defaultfont = 'Dejavu Sans'

def draw(drawsurface, string, region, color=defaultcolor, size=defaultsize, font=defaultfont, xcentered=True, ycentered=True):
    '''Render a text string onto drawsurface, within region'''
    font = pygame.font.SysFont(font, size)
    textbitmap = font.render(string, True, color)
    xoffset = 0
    yoffset = region.height-(size*1.25)                   # Clunky - FIXME
    if xcentered:
        xoffset = (region.width - textbitmap.get_width())/2
    if ycentered:
        yoffset = (region.height - textbitmap.get_height())/2
    outputbitmap = pygame.Surface(region.size, pygame.SRCALPHA, 32)
    outputbitmap.blit(textbitmap, (xoffset, yoffset))
    drawsurface.blit(outputbitmap, region)
