import pygame
import images
import TextBox
import newTextBox
import collectables
from colors import *

class ScoreWidget:
    '''Widget to show a score and associated image'''
    def __init__(self, image, window, total=None, stringfunc=None):
        self.image = image
        self.window = window
        self.prevarea = None
        self.total = total
        self.stringfunc = (stringfunc if stringfunc != None else
                           lambda a, b: str(a) + ("/"+str(b) if b != None else ""))
    
    def draw(self, area, quantity):
        '''Draw the score widget'''
        area = pygame.Rect(area)
        pygame.draw.rect(self.window, WHITE, area)
        pygame.draw.rect(self.window, GREY, area, 1)
        imagearea = area.inflate(-10,-10)
        imagearea.height -= 20
        if imagearea.height > 0 and imagearea.height > 0:
            fittedimage = self.image.get_rect().fit(imagearea)
            self.window.blit(pygame.transform.scale(self.image, fittedimage.size), fittedimage)
        string = self.stringfunc(quantity, self.total)
        newTextBox.Draw(self.window, string, area, colour=BLACK, size=18, ycentred=False)


class MinimapWidget:
    '''Widget to display a small map of the world'''
    def __init__(self, world, window):
        self.world = world
        self.window = window

    def draw(self, area, scrollpos):
        '''Draw the minimap'''
        area = pygame.Rect(area)
        miniworldScale = min(float(area.width)/(self.world.cellmap.size[0]*images.BLOCKSIZE),
                             float(area.height)/(self.world.cellmap.size[1]*images.BLOCKSIZE))
        miniworld = pygame.transform.scale(self.world.surface, (int(self.world.cellmap.size[0]*images.BLOCKSIZE*miniworldScale), int(self.world.cellmap.size[1]*images.BLOCKSIZE*miniworldScale)))
        old_clip = self.window.get_clip()
        self.window.set_clip(area.left, area.top, int(self.world.cellmap.size[0]*images.BLOCKSIZE*miniworldScale), int(self.world.cellmap.size[1]*images.BLOCKSIZE*miniworldScale))
        self.window.blit(miniworld, area)
        for tx in [scrollpos[0]-self.world.surface.get_width(), scrollpos[0], scrollpos[0]+self.world.surface.get_width()]:
            for ty in [scrollpos[1]-self.world.surface.get_height(), scrollpos[1], scrollpos[1]+self.world.surface.get_height()]:
                pygame.draw.rect(self.window,
                    self.world.player.color,
                    (area.left-(tx*miniworldScale), # Top x corner of minimap, plus scroll offset
                    area.top-(ty*miniworldScale), # Top y ''
                    #FIXME should be viewport size, not window size!
                    1+ self.window.get_width()*miniworldScale,
                    1+ self.window.get_height()*miniworldScale),
                    1)
        self.window.set_clip(old_clip)

class HUD:
    '''Vertical bar with player scores and minimap'''
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.coinwidget = ScoreWidget(images.HudCoin, window, world.cellmap.origcoins)
        self.chocwidget = ScoreWidget(images.HudChoc, window,
                                      stringfunc=lambda a, b: str(round(a/1000.0, 2))+"kg" if a >= 1000 else str(a)+"g")
        self.dynamitewidget = ScoreWidget(images.HudDynamite, window)
        self.minimapwidget = MinimapWidget(world, window)

    def draw(self, area, scrollpos):
        '''Draw the heads-up display'''
        area = pygame.Rect(area)
        pygame.draw.rect(self.window, BLACK, area)
        border = 2
        widgetwidth = area.width-border
        scoreheight = area.height-widgetwidth-2 # Leave space for the HUD
        widgetheight = (scoreheight-4)/3
        self.coinwidget.draw((area.left+border, area.top, widgetwidth, widgetheight), self.world.player.score[collectables.COIN])
        self.chocwidget.draw((area.left+border, area.top+border+widgetheight, widgetwidth, widgetheight), self.world.player.score[collectables.CHOCOLATE])
        self.dynamitewidget.draw((area.left+border, area.top+2*border+2*widgetheight, widgetwidth, widgetheight), self.world.player.score[collectables.DYNAMITE])
        self.minimapwidget.draw((area.left+border, area.bottom-widgetwidth, widgetwidth, widgetwidth), scrollpos)
    
    def endsplash(self, reason):
        '''Display a splash message across the entire window'''
        def splash(message):
            pygame.draw.rect(self.window, BLACK, self.window.get_rect())
            newTextBox.Draw(self.window, message, self.window.get_rect(), colour=WHITE, size=40)
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
