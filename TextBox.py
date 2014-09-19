import pygame
from colors import *

defaultfont = "./fonts/MorrisRomanBlack.ttf" #'Dejavu Sans'

def draw(drawsurface, string, region, size, color, font=defaultfont, xcentered=True, ycentered=True, beveled=False):
    outputbitmap = pygame.Surface((region.width, region.height), pygame.SRCALPHA, 32)
    font = pygame.font.Font(font, size)
    maincolor = pygame.Color(color[0], color[1], color[2])
    maincolor = maincolor.correct_gamma(1) 
    darkcolor = BLACK # maincolor.correct_gamma(8)
    lightcolor = maincolor.correct_gamma(8)
    for (xbeveloffset, ybeveloffset, color) in ((1, 1, darkcolor), (1, -1, lightcolor), (-1, 1, darkcolor), (-1, -1, lightcolor), (0, 0, maincolor)) if beveled else ((0, 0, color),):
        xoffset = xbeveloffset
        yoffset = ybeveloffset + region.height-size                   # Clunky - FIXME
        textbitmap = font.render(string, True, color)
        if xcentered:
            xoffset = xbeveloffset + (region.width - textbitmap.get_width())/2
        if ycentered:
            yoffset = ybeveloffset + (region.height - textbitmap.get_height())/2
        outputbitmap.blit(textbitmap, (xoffset, yoffset))
    drawsurface.blit(outputbitmap, region.topleft)
