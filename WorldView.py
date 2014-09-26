from images import TILESIZE
import pygame

class WorldView:
    def __init__(self, world, window):
        self.scrollpos = None

    def draw(self, region, world, window):
        if self.scrollpos == None:
            self.scrollpos = [(-TILESIZE*world.player.position[0])+region.width/2,
                              (-TILESIZE*world.player.position[1])+region.height/2]
        drawregion = region.copy()
        def updateregion():
            drawregion.width = min(world.surface.get_width(), region.width)
            drawregion.height = min(world.surface.get_height(), region.height)
            drawregion.center = region.center

        def updatescrollpos():
            '''scroll towards the correct position'''
            for axis in [0, 1]:
                pq = (world.player.position[axis]*TILESIZE+self.scrollpos[axis]) % world.surface.get_size()[axis]
                if drawregion.size[axis] > 2*world.player.visibility*TILESIZE:
                    dr = (world.player.visibility*TILESIZE, drawregion.size[axis]-(world.player.visibility+1)*TILESIZE)
                else:
                    dr = [drawregion.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % world.surface.get_size()[axis]

        def blitworld():
            oldclip = window.get_clip()
            window.set_clip(drawregion)
            for tx in [self.scrollpos[0]-world.surface.get_width(), self.scrollpos[0], self.scrollpos[0]+world.surface.get_width()]:
                tx += drawregion.left
                for ty in [self.scrollpos[1]-world.surface.get_height(), self.scrollpos[1], self.scrollpos[1]+world.surface.get_height()]:
                    ty += drawregion.top
                    if world.surface.get_rect(topleft=(tx, ty)).colliderect(drawregion):
                        window.blit(world.surface, (tx, ty))
            window.set_clip(oldclip)

        updateregion()
        updatescrollpos()
        blitworld()
        return self.scrollpos
