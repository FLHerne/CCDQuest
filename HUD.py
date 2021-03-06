import pygame
import hudimages
from TextBox import TextBox
import collectables
from colors import *

class ScoreWidget:
    """Widget to show a score and associated image"""
    def __init__(self, image, window, stringfunc=None, bgtileimage=None):
        self.image = image
        self.bgtileimage = bgtileimage
        self.window = window
        self.stringfunc = (stringfunc if stringfunc != None else
                           lambda a, b: str(a) + ("/"+str(b) if b != None else ""))
        self.textbox = TextBox(22, (205, 205, 75), True)

    def draw(self, region, quantity, total=None):
        """Draw the score widget"""
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
        string = self.stringfunc(quantity, total)
        self.textbox.draw(string, region, (True, False), self.window)
        self.window.set_clip(old_clip)

class MinimapWidget:
    """Widget to display a small map of the world"""
    def __init__(self, player, window):
        self.player = player
        self.window = window

    def draw(self, region, scrollpos):
        """Draw the minimap"""
        geplayer = self.player.geplayer
        surface = geplayer.surface
        region = pygame.Rect(region)
        old_clip = self.window.get_clip()
        self.window.set_clip(region)
        miniworldscale = min(float(region.width)/surface.get_width(),
                             float(region.height)/surface.get_height())
        miniworld = pygame.transform.scale(surface,
                                           (int(surface.get_width()*miniworldscale),
                                            int(surface.get_height()*miniworldscale)))
        self.window.blit(miniworld, region)
        for tx in [scrollpos[0]-surface.get_width(), scrollpos[0], scrollpos[0]+surface.get_width()]:
            for ty in [scrollpos[1]-surface.get_height(), scrollpos[1], scrollpos[1]+surface.get_height()]:
                pygame.draw.rect(self.window,
                    geplayer.color,
                    (region.left-(tx*miniworldscale), # Top x corner of minimap, plus scroll offset
                    region.top-(ty*miniworldscale), # Top y ''
                    #FIXME should be viewport size, not window size!
                    1+ self.window.get_width()*miniworldscale,
                    1+ self.window.get_height()*miniworldscale),
                    1)
        self.window.set_clip(old_clip)

class Frame:
    """Thingy to draw around widgets"""
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, images, window):
        self.images = images
        self.thickness = (images[Frame.HORIZONTAL].get_height(),
                          images[Frame.VERTICAL].get_width())
        self.window = window

    def draw(self, region, orientation):
        """Draw frame along top or left of region"""
        region = pygame.Rect(region)
        old_clip = self.window.get_clip()
        self.window.set_clip(region)
        drawpoint = list(region.topleft)
        while region.collidepoint(drawpoint):
            self.window.blit(self.images[orientation], drawpoint)
            drawpoint[orientation] += self.images[orientation].get_size()[orientation]
        self.window.set_clip(old_clip)

class HUD:
    """Vertical bar with player scores and minimap"""
    def __init__(self, player, window):
        self.player = player
        self.window = window
        self.frame = Frame((hudimages.FrameHoriz, hudimages.FrameVert), window)
        self.coinwidget = ScoreWidget(hudimages.Coin, window, bgtileimage=hudimages.HudBackground)
        self.chocwidget = ScoreWidget(hudimages.Choc, window,
                                      stringfunc=lambda a, b: str(round(a/1000.0, 2))+"kg" if a >= 1000 else str(a)+"g",
                                      bgtileimage=hudimages.HudBackground)
        self.dynamitewidget = ScoreWidget(hudimages.Dynamite, window, bgtileimage=hudimages.HudBackground)
        self.minimapwidget = MinimapWidget(player, window)

    def draw(self, region, scrollpos):
        """Draw the heads-up display"""
        with self.player.statelock:
            geplayer = self.player.geplayer
        if geplayer is None:
            return False
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
        self.dynamitewidget.draw(widgetareas[0], geplayer.score[collectables.DYNAMITE])
        self.chocwidget.draw(widgetareas[1], geplayer.score[collectables.CHOCOLATE])
        self.coinwidget.draw(widgetareas[2], geplayer.score[collectables.COIN], geplayer.cellmap.origcoins) #FIXME crazy indirection.
