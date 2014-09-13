import pygame
from colors import *

def draw(drawsurface, string, region, colour=YELLOW, size=12, font="./fonts/MorrisRomanBlack.ttf", xcentered=True, ycentered=True, beveled=False):
    outputbitmap = pygame.Surface(region.size(), pygame.SRCALPHA, 32)
    font = pygame.font.Font(font, size)
    darkcolour = BLACK
    maincolour = YELLOW
    lightcolour = DARKYELLOW
    for x3doffset, y3doffset, colour in ((1, 1, darkcolour), (-1, -1, lightcolour), (0, 0, maincolour) if beveled else (0, 0, maincolour)):
        xoffset = x3doffset
        yoffset = y3doffset + region.height-(size*1.25)                   # Clunky - FIXME
        textbitmap = font.render(string, True, colour)
        if xcentered:
            xoffset = x3doffset + (region.width - textbitmap.get_width())/2
        if ycentered:
            yoffset = y3doffset + (region.height - textbitmap.get_height())/2
        outputbitmap.blit(textbitmap, (xoffset, yoffset))
    drawsurface.blit(outputbitmap, region)

