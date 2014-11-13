from images import TILESIZE
from colors import *
import pygame
import gamestate

class WorldView:
    def __init__(self, window):
        self.window = window
        self.scrollpos = None

    def draw(self, region):
        self.world = gamestate.currentworld
        if self.scrollpos == None:
            self.scrollpos = [(-TILESIZE*self.world.player.position[0])+region.width/2,
                              (-TILESIZE*self.world.player.position[1])+region.height/2]
        drawregion = region.copy()
        def updateregion():
            drawregion.width = min(self.world.surface.get_width(), region.width)
            drawregion.height = min(self.world.surface.get_height(), region.height)
            drawregion.center = region.center

        def updatescrollpos():
            """scroll towards the correct position"""
            for axis in [0, 1]:
                pq = (self.world.player.position[axis]*TILESIZE+self.scrollpos[axis]) % self.world.surface.get_size()[axis]
                if drawregion.size[axis] > 2*self.world.player.visibility*TILESIZE:
                    dr = (self.world.player.visibility*TILESIZE, drawregion.size[axis]-(self.world.player.visibility+1)*TILESIZE)
                else:
                    dr = [drawregion.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % self.world.surface.get_size()[axis]

        def blitworld():
            if drawregion.size < region.size:
                pygame.draw.rect(self.window, BLACK, region)
            oldclip = self.window.get_clip()
            self.window.set_clip(drawregion)
            for tx in [self.scrollpos[0]-self.world.surface.get_width(), self.scrollpos[0], self.scrollpos[0]+self.world.surface.get_width()]:
                tx += drawregion.left
                for ty in [self.scrollpos[1]-self.world.surface.get_height(), self.scrollpos[1], self.scrollpos[1]+self.world.surface.get_height()]:
                    ty += drawregion.top
                    if self.world.surface.get_rect(topleft=(tx, ty)).colliderect(drawregion):
                        self.window.blit(self.world.surface, (tx, ty))
            self.window.set_clip(oldclip)

        updateregion()
        updatescrollpos()
        blitworld()
        return self.scrollpos
