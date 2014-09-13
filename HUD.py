import pygame
import images
import TextBox
import collectables
from colors import *

class ScoreWidget:
    '''Widget to show a score and associated image'''
    def __init__(self, image, window, total=None, stringfunc=None, bgtileimage=None):
        self.image = image
        self.bgtileimage = bgtileimage
        self.window = window
        self.total = total
        self.stringfunc = (stringfunc if stringfunc != None else
                           lambda a, b: str(a) + ("/"+str(b) if b != None else ""))

    def draw(self, region, quantity):
        '''Draw the score widget'''
        region = pygame.Rect(region)
        old_clip = self.window.get_clip()
        self.window.set_clip(region)
        if self.bgtileimage:
            for ix in range(region.left, region.right, self.bgtileimage.get_width()):
                for iy in range(region.top, region.bottom, self.bgtileimage.get_height()):
                    self.window.blit(self.bgtileimage, (ix, iy))
        else:
            pygame.draw.rect(self.window, GREY, region)
        imageregion = region.inflate(-10,-10)
        imageregion.height -= 20
        if imageregion.height > 0 and imageregion.height > 0:
            fittedimage = self.image.get_rect().fit(imageregion)
            self.window.blit(pygame.transform.scale(self.image, fittedimage.size), fittedimage)
        string = self.stringfunc(quantity, self.total)
        TextBox.draw(self.window, string, region, size=22, ycentered=False, beveled=True)
        self.window.set_clip(old_clip)

class MinimapWidget:
    '''Widget to display a small map of the world'''
    def __init__(self, world, window):
        self.world = world
        self.window = window

    def draw(self, region, scrollpos):
        '''Draw the minimap'''
        region = pygame.Rect(region)
        old_clip = self.window.get_clip()
        self.window.set_clip(region)
        miniworldScale = min(float(region.width)/(self.world.cellmap.size[0]*images.BLOCKSIZE),
                             float(region.height)/(self.world.cellmap.size[1]*images.BLOCKSIZE))
        miniworld = pygame.transform.scale(self.world.surface, (int(self.world.cellmap.size[0]*images.BLOCKSIZE*miniworldScale), int(self.world.cellmap.size[1]*images.BLOCKSIZE*miniworldScale)))
        self.window.blit(miniworld, region)
        for tx in [scrollpos[0]-self.world.surface.get_width(), scrollpos[0], scrollpos[0]+self.world.surface.get_width()]:
            for ty in [scrollpos[1]-self.world.surface.get_height(), scrollpos[1], scrollpos[1]+self.world.surface.get_height()]:
                pygame.draw.rect(self.window,
                    self.world.player.color,
                    (region.left-(tx*miniworldScale), # Top x corner of minimap, plus scroll offset
                    region.top-(ty*miniworldScale), # Top y ''
                    #FIXME should be viewport size, not window size!
                    1+ self.window.get_width()*miniworldScale,
                    1+ self.window.get_height()*miniworldScale),
                    1)
        self.window.set_clip(old_clip)

class Frame:
    '''Thingy to draw around widgets'''
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, images, window):
        self.images = images
        self.thickness = (images[Frame.HORIZONTAL].get_height(),
                          images[Frame.VERTICAL].get_width())
        self.window = window

    def draw(self, region, orientation):
        region = pygame.Rect(region)
        old_clip = self.window.get_clip()
        self.window.set_clip(region)
        if orientation == Frame.HORIZONTAL:
            for ix in range(region.left, region.right, self.images[orientation].get_width()):
                self.window.blit(self.images[orientation], (ix, region.top))
        else:
            for iy in range(region.top, region.bottom, self.images[orientation].get_height()):
                self.window.blit(self.images[orientation], (region.left, iy))
        self.window.set_clip(old_clip)

class HUD:
    '''Vertical bar with player scores and minimap'''
    def __init__(self, world, window, bgtileimage=None):
        self.window = window
        self.world = world
        self.bgtileimage = bgtileimage
        self.frame = Frame((images.HudFrameHoriz, images.HudFrameVert), window)
        self.coinwidget = ScoreWidget(images.HudCoin, window, world.cellmap.origcoins)
        self.chocwidget = ScoreWidget(images.HudChoc, window,
                                      stringfunc=lambda a, b: str(round(a/1000.0, 2))+"kg" if a >= 1000 else str(a)+"g")
        self.dynamitewidget = ScoreWidget(images.HudDynamite, window)
        self.minimapwidget = MinimapWidget(world, window)

    def draw(self, region, scrollpos):
        '''Draw the heads-up display'''
        region = pygame.Rect(region)
        if self.bgtileimage:
            for ix in range(region.left, region.right, self.bgtileimage.get_width()):
                for iy in range(region.top, region.bottom, self.bgtileimage.get_height()):
                    self.window.blit(self.bgtileimage, (ix, iy))
        else:
            pygame.draw.rect(self.window, BLACK, region)
        VERTICAL = Frame.VERTICAL
        HORIZONTAL = Frame.HORIZONTAL
        framewidth = self.frame.thickness[VERTICAL]
        frameheight = self.frame.thickness[HORIZONTAL]
        widgetwidth = region.width-framewidth
        self.frame.draw((region.left, region.top, framewidth, region.height), VERTICAL)
        self.minimapwidget.draw((region.left+framewidth, region.bottom-widgetwidth, widgetwidth, widgetwidth), scrollpos)
        scoreheight = region.height-3*frameheight-widgetwidth
        widgetheight = int(scoreheight/3)
        self.coinwidget.draw((region.left+framewidth, region.top, widgetwidth, widgetheight), self.world.player.score[collectables.COIN])
        self.frame.draw((region.left, region.top+widgetheight, region.width, frameheight), HORIZONTAL)
        self.chocwidget.draw((region.left+framewidth, region.top+frameheight+widgetheight, widgetwidth, widgetheight), self.world.player.score[collectables.CHOCOLATE])
        self.frame.draw((region.left, region.top+2*widgetheight+frameheight, region.width, frameheight), HORIZONTAL)
        self.dynamitewidget.draw((region.left+framewidth, region.top+2*(frameheight+widgetheight), widgetwidth, widgetheight), self.world.player.score[collectables.DYNAMITE])
        self.frame.draw((region.left, region.top+3*widgetheight+2*frameheight, region.width, frameheight), HORIZONTAL)

    def endsplash(self, reason):
        '''Display a splash message across the entire window'''
        def splash(message):
            pygame.draw.rect(self.window, BLACK, self.window.get_rect())
            TextBox.draw(self.window, message, self.window.get_rect(), color=WHITE, size=40)
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
            
