import pygame
from colors import *

defaultSize = 12
defaultColour = YELLOW
defaultFont = "./fonts/MorrisRomanBlack.ttf" #'Dejavu Sans'

def Draw(drawSurface, textString, rect, colour=defaultColour, size=defaultSize, font=defaultFont, xcentred=True, ycentred=True, beveled=False):
    outputBitmap = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
    font = pygame.font.Font(font, size)
    darkcolour = BLACK
    maincolour = YELLOW
    lightcolour = DARKYELLOW
    for x3doffset, y3doffset, colour in ((1, 1, darkcolour), (-1, -1, lightcolour), (0, 0, maincolour) if beveled else (0, 0, maincolour)):
        xoffset = x3doffset
        yoffset = y3doffset + rect.height-(size*1.25)                   # Clunky - FIXME
        textBitmap = font.render(textString, True, colour)
        if xcentred:
            xoffset = x3doffset + (rect.width - textBitmap.get_width())/2
        if ycentred:
            yoffset = y3doffset + (rect.height - textBitmap.get_height())/2
        
        outputBitmap.blit(textBitmap, (xoffset, yoffset))

    drawSurface.blit(outputBitmap, rect.topleft)
    
