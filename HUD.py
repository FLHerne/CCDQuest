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
            pygame.draw.rect(self.window, BLACK, region)
        imageregion = region.inflate(-10,-10)
        imageregion.height -= 20
        if imageregion.height > 0 and imageregion.height > 0:
            fittedimage = self.image.get_rect().fit(imageregion)
            self.window.blit(pygame.transform.scale(self.image, fittedimage.size), fittedimage)
        string = self.stringfunc(quantity, self.total)
        TextBox.draw(self.window, string, region, size=22, color=(205, 205, 75), ycentered=False, beveled=True)
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
        drawpoint = list(region.topleft)
        while region.collidepoint(drawpoint):
            self.window.blit(self.images[orientation], drawpoint)
            drawpoint[orientation] += self.images[orientation].get_size()[orientation]
        self.window.set_clip(old_clip)

class HUD:
    '''Vertical bar with player scores and minimap'''
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.frame = Frame((images.HudFrameHoriz, images.HudFrameVert), window)
        self.coinwidget = ScoreWidget(images.HudCoin, window, world.cellmap.origcoins, bgtileimage=images.HudBackground)
        self.chocwidget = ScoreWidget(images.HudChoc, window,
                                      stringfunc=lambda a, b: str(round(a/1000.0, 2))+"kg" if a >= 1000 else str(a)+"g",
                                      bgtileimage=images.HudBackground)
        self.dynamitewidget = ScoreWidget(images.HudDynamite, window, bgtileimage=images.HudBackground)
        self.minimapwidget = MinimapWidget(world, window)

    def draw(self, region, scrollpos):
        '''Draw the heads-up display'''
        region = pygame.Rect(region)
        pygame.draw.rect(self.window, BLACK, region)
        framewidth = self.frame.thickness[Frame.VERTICAL]
        frameheight = self.frame.thickness[Frame.HORIZONTAL]
        widgetwidth = region.width-framewidth
        self.frame.draw(region, Frame.VERTICAL)

        self.frame.draw(region.move(0, region.height-framewidth), Frame.HORIZONTAL)
        self.minimapwidget.draw((region.left+framewidth, region.bottom-widgetwidth-framewidth, widgetwidth, widgetwidth), scrollpos)
        region.height -= widgetwidth+(2*framewidth)
        self.frame.draw(region.move(0, region.height), Frame.HORIZONTAL)
        widgetareas = []
        for iy in range(0, 3):
            offset_y = int(iy*region.height/3)
            self.frame.draw(region.move(0, offset_y), Frame.HORIZONTAL)
            widgetareas.append((region.left+framewidth, region.top+offset_y+frameheight,
                                widgetwidth, (region.height/3)-frameheight+1))
        self.dynamitewidget.draw(widgetareas[0], self.world.player.score[collectables.DYNAMITE])
        self.chocwidget.draw(widgetareas[1], self.world.player.score[collectables.CHOCOLATE])
        self.coinwidget.draw(widgetareas[2], self.world.player.score[collectables.COIN])

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