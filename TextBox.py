import pygame
from colors import *

defaultFont = "./fonts/MorrisRomanBlack.ttf" #'Dejavu Sans'

def draw(drawSurface, textString, region, size, color, font=defaultFont, xcentered=True, ycentered=True, beveled=False):
    outputBitmap = pygame.Surface((region.width, region.height), pygame.SRCALPHA, 32)
    font = pygame.font.Font(font, size)
    maincolor = pygame.Color(color[0], color[1], color[2])
    darkcolor = BLACK # maincolor.correct_gamma(10)
    lightcolor = WHITE # maincolor.correct_gamma(0.1)
    for (xbeveloffset, ybeveloffset, color) in ((1, 1, darkcolor), (-1, -1, lightcolor), (0, 0, maincolor)) if beveled else ((0, 0, color),):
        xoffset = xbeveloffset
        yoffset = ybeveloffset + region.height-size                   # Clunky - FIXME
        textBitmap = font.render(textString, True, color)
        if xcentered:
            xoffset = xbeveloffset + (region.width - textBitmap.get_width())/2
        if ycentered:
            yoffset = ybeveloffset + (region.height - textBitmap.get_height())/2
        
        outputBitmap.blit(textBitmap, (xoffset, yoffset))

    drawSurface.blit(outputBitmap, region.topleft)
    
