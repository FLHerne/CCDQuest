import pygame
from colours import *

defaultSize = 14
defaultColour = WHITE
defaultFont = 'Monospace'

def Draw(drawSurface, textString, rect, colour=defaultColour, centred=True):
    size = defaultSize
    font = pygame.font.SysFont(defaultFont, defaultSize)
    textBitmap = font.render(textString, True, colour)
    if centred:
        offset = ((rect.width - textBitmap.get_width())/2, (rect.height - textBitmap.get_height())/2)
    else:
        offset = (0, 0)
    outputBitmap = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
    outputBitmap.blit(textBitmap, offset)
    
    drawSurface.blit(outputBitmap, rect.topleft)
    
