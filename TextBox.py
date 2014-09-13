import pygame
from colors import *

defaultFont = "./fonts/MorrisRomanBlack.ttf" #'Dejavu Sans'

def draw(drawSurface, textString, rect, size, colour, font=defaultFont, xcentered=True, ycentered=True, beveled=False):
    outputBitmap = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
    font = pygame.font.Font(font, size)
    maincolour = pygame.Color(colour[0], colour[1], colour[2])
    darkcolour = BLACK # maincolour.correct_gamma(10)
    lightcolour = WHITE # maincolour.correct_gamma(0.1)
    for (xbeveloffset, ybeveloffset, colour) in ((1, 1, darkcolour), (-1, -1, lightcolour), (0, 0, maincolour)) if beveled else ((0, 0, colour),):
        xoffset = xbeveloffset
        yoffset = ybeveloffset + rect.height-size                   # Clunky - FIXME
        textBitmap = font.render(textString, True, colour)
        if xcentered:
            xoffset = xbeveloffset + (rect.width - textBitmap.get_width())/2
        if ycentered:
            yoffset = ybeveloffset + (rect.height - textBitmap.get_height())/2
        
        outputBitmap.blit(textBitmap, (xoffset, yoffset))

    drawSurface.blit(outputBitmap, rect.topleft)
    
