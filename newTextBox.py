import pygame
from colors import *

defaultSize = 12
defaultColour = WHITE
defaultFont = "./fonts/morris_roman/MorrisRomanBlack.ttf" #'Dejavu Sans'

def Draw(drawSurface, textString, rect, colour=defaultColour, size=defaultSize, font=defaultFont, xcentred=True, ycentred=True):
    font = pygame.font.Font(font, size)
    textBitmap = font.render(textString, True, colour)
    xoffset = 0
    yoffset = rect.height-(size*1.25)                   # Clunky - FIXME
    if xcentred:
        xoffset = (rect.width - textBitmap.get_width())/2
    if ycentred:
        yoffset = (rect.height - textBitmap.get_height())/2
        
    outputBitmap = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
    outputBitmap.blit(textBitmap, (xoffset, yoffset))
    
    drawSurface.blit(outputBitmap, rect.topleft)
    
