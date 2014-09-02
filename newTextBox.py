import pygame

def TextBox(textString, size, rect, colour=BLACK, centred = True)
    font = pygame.font.Font(None, size)
    #printedSize = font.size(textstring)
    textBitmap = font.render(textString, true, colour)
    offset = ((rect.width - textBitmap.get_width())/2, (rect.height - textBitmap.get_height())/2)
    outputBitmap = pygame.Surface(rect.width, rect.height)
    outputBitmap.blit(textBitmap, offset)
    return outputBitmap