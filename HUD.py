import pygame
import images
import TextBox
import collectables
from colors import *

class ScoreWidget:
    '''Widget to show a score and assosciated image'''
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
        imagearea = area.inflate(-10,-10)
        imagearea.height -= 20
        if imagearea.height > 0 and imagearea.height > 0:
            fittedimage = self.image.get_rect().fit(imagearea)
            self.window.blit(pygame.transform.scale(self.image, fittedimage.size), fittedimage)
        string = self.stringfunc(quantity, self.total)
        TextBox.Print(self.window, False,
                        area.left, area.bottom-25, area.width,
                        None, BLACK, 'Arial', 20,
                        string,
                        True, [False, area.height])

class MinimapWidget:
    '''Widget to display a small map of the whole world'''
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
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.coinwidget = ScoreWidget(images.HudCoin, window, world.cellmap.origcoins)
        self.chocwidget = ScoreWidget(images.HudChoc, window,
                                      stringfunc=lambda a, b: str(round(a/1000.0, 2))+"kg" if a >= 1000 else str(a)+"g")
        self.dynamitewidget = ScoreWidget(images.HudDynamite, window)
        self.minimapwidget = MinimapWidget(world, window)
        #str(round(self.world.player.score[collectables.CHOCOLATE] / 1000.0, 2)) + "kg"

    def draw(self, area, scrollpos):
        '''Draw the heads-up display, with current information'''
        area = pygame.Rect(area)
        pygame.draw.rect(self.window, BLACK, area)
        scoreheight = area.height - 92 # Leave space for the HUD
        widgetheight = (scoreheight-4)/3
        self.coinwidget.draw((area.left+2, area.top, 90, widgetheight), self.world.player.score[collectables.COIN])
        self.chocwidget.draw((area.left+2, area.top+2+widgetheight, 90, widgetheight), self.world.player.score[collectables.CHOCOLATE])
        self.dynamitewidget.draw((area.left+2, area.top+4+2*widgetheight, 90, widgetheight), self.world.player.score[collectables.DYNAMITE])
        self.minimapwidget.draw((area.left+2, area.bottom-90, 90, 90), scrollpos)
    
    def endsplash(self, reason):
        '''Display a splash message across the entire window'''
        def splash(message):
            TextBox.Print(self.window, False,
                          0, 0, self.window.get_width(),
                          BLACK, WHITE, 'Arial', 40,
                          message,
                          True, [True, self.window.get_height()])
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
