from images import TILESIZE
from hudimages import HourGlass
from TextBox import TextBox
from colors import *
import pygame

class WorldView:
    def __init__(self, player, window):
        self.player = player
        self.window = window
        self.world = None
        self.scrollpos = None

    def draw(self, region):
        state = self.player.state
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
                splash("Loading "+self.player, 25, HourGlass)
            return self.scrollpos
        world = self.player.world
        worldsurface = world.surfaces[self.player]
        if world != self.world:
            self.scrollpos = None
            self.world = world
        if self.scrollpos == None:
            self.scrollpos = [(-TILESIZE*self.player.position[0])+region.width/2,
                              (-TILESIZE*self.player.position[1])+region.height/2]
        drawregion = region.copy()
        def updateregion():
            drawregion.width = min(worldsurface.get_width(), region.width)
            drawregion.height = min(worldsurface.get_height(), region.height)
            drawregion.center = region.center

        def updatescrollpos():
            """scroll towards the correct position"""
            for axis in [0, 1]:
                pq = (self.player.position[axis]*TILESIZE+self.scrollpos[axis]) % worldsurface.get_size()[axis]
                if drawregion.size[axis] > 2*self.player.visibility*TILESIZE:
                    dr = (self.player.visibility*TILESIZE, drawregion.size[axis]-(self.player.visibility+1)*TILESIZE)
                else:
                    dr = [drawregion.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % worldsurface.get_size()[axis]

        def blitworld():
            if drawregion.size < region.size:
                pygame.draw.rect(self.window, BLACK, region)
            oldclip = self.window.get_clip()
            self.window.set_clip(drawregion)
            for tx in [self.scrollpos[0]-worldsurface.get_width(), self.scrollpos[0], self.scrollpos[0]+worldsurface.get_width()]:
                tx += drawregion.left
                for ty in [self.scrollpos[1]-worldsurface.get_height(), self.scrollpos[1], self.scrollpos[1]+worldsurface.get_height()]:
                    ty += drawregion.top
                    if worldsurface.get_rect(topleft=(tx, ty)).colliderect(drawregion):
                        self.window.blit(worldsurface, (tx, ty))
            self.window.set_clip(oldclip)

        updateregion()
        updatescrollpos()
        blitworld()
        return self.scrollpos
