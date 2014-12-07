from images import TILESIZE
from hudimages import HourGlass
from TextBox import TextBox
from colors import *
import pygame
import time
import random

class WorldView:
    def __init__(self, player, window):
        self.player = player
        self.window = window
        self.geplayer = None
        self.scrollpos = None
        self.progress = 0.0

    def draw(self, region):
        with self.player.statelock:
            state = self.player.state
            mapdef = self.player.mapdef
            geplayer = self.player.geplayer
        if state != 'normal':
            def splash(message, fontsize=40, icon=None):
                """Display a splash message across the viewing area"""
                pygame.draw.rect(self.window, BLACK, region)
                textbox = TextBox(fontsize, WHITE, False)
                if icon is not None:
                    self.window.blit(icon, [(region.size[axis]-icon.get_size()[axis])/2 for axis in [0,1]])
                    region.move_ip(0, icon.get_height()/2 + fontsize)
                textbox.draw(message, region, surface=self.window)
            if state == 'lost':
                splash("You lost!")
            elif state == 'won':
                splash("You won!")
            elif state == 'loading':
                loadingicon = pygame.Surface(HourGlass.get_size())
                loadingicon.fill(BLACK)
                scaledprogress = self.progress*loadingicon.get_height()
                loadingiconrect = loadingicon.get_rect()
                upperrect = ((loadingiconrect.left, loadingiconrect.top+scaledprogress), (loadingiconrect.width, loadingiconrect.centery-scaledprogress))
                lowerrect = ((loadingiconrect.left, loadingiconrect.bottom-scaledprogress), loadingiconrect.midright)
                pygame.draw.rect(loadingicon, DARKYELLOW, upperrect)
                pygame.draw.rect(loadingicon, DARKYELLOW, lowerrect)
                pygame.draw.line(loadingicon, DARKYELLOW, loadingiconrect.center, (loadingiconrect.centerx+random.randint(-3, 3), loadingiconrect.height))
                loadingicon.blit(HourGlass, (0, 0))
                splash("Loading "+mapdef['name'], 25, loadingicon)
                if self.progress < 1:
                    self.progress += 0.02
                else:
                    self.progress = 0
            elif state == 'crashed':
                splash("Game crashed!")
            return self.scrollpos
        if geplayer is not self.geplayer:
            self.geplayer = geplayer
            self.scrollpos = None
        surface = geplayer.surface
        if self.scrollpos == None:
            self.scrollpos = [(-TILESIZE*geplayer.position[0])+region.width/2,
                              (-TILESIZE*geplayer.position[1])+region.height/2]
        drawregion = region.copy()
        def updateregion():
            drawregion.width = min(surface.get_width(), region.width)
            drawregion.height = min(surface.get_height(), region.height)
            drawregion.center = region.center

        def updatescrollpos():
            """scroll towards the correct position"""
            for axis in [0, 1]:
                pq = (geplayer.position[axis]*TILESIZE+self.scrollpos[axis]) % surface.get_size()[axis]
                if drawregion.size[axis] > 2*geplayer.visibility*TILESIZE:
                    dr = (geplayer.visibility*TILESIZE, drawregion.size[axis]-(geplayer.visibility+1)*TILESIZE)
                else:
                    dr = [drawregion.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % surface.get_size()[axis]

        def blitworld():
            if drawregion.size < region.size:
                pygame.draw.rect(self.window, BLACK, region)
            oldclip = self.window.get_clip()
            self.window.set_clip(drawregion)
            for tx in [self.scrollpos[0]-surface.get_width(), self.scrollpos[0], self.scrollpos[0]+surface.get_width()]:
                tx += drawregion.left
                for ty in [self.scrollpos[1]-surface.get_height(), self.scrollpos[1], self.scrollpos[1]+surface.get_height()]:
                    ty += drawregion.top
                    if surface.get_rect(topleft=(tx, ty)).colliderect(drawregion):
                        self.window.blit(surface, (tx, ty))
            self.window.set_clip(oldclip)

        updateregion()
        updatescrollpos()
        blitworld()
        return self.scrollpos
