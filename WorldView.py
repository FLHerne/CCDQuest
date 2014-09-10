from images import BLOCKSIZE
import pygame

class WorldView:
    def __init__(self, world, window):
        self.scrollpos = None
    
    def draw(self, area, world, window):
        if self.scrollpos == None:
            self.scrollpos = [(-BLOCKSIZE*world.player.position[0])+area.width/2,
                              (-BLOCKSIZE*world.player.position[1])+area.height/2]
        dare = area.copy()
        def updatearea():
            dare.width = min(world.surface.get_width(), area.width)
            dare.height = min(world.surface.get_height(), area.height)
            dare.center = area.center

        def updatescrollpos():
            '''scroll towards the correct position'''
            for axis in [0, 1]:
                pq = (world.player.position[axis]*BLOCKSIZE+self.scrollpos[axis]) % world.surface.get_size()[axis]
                if world.surface.get_size()[axis] > 2*world.player.visibility*BLOCKSIZE:
                    dr = (world.player.visibility*BLOCKSIZE, dare.size[axis]-(world.player.visibility+1)*BLOCKSIZE)
                else:
                    dr = [dare.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % world.surface.get_size()[axis]

        def blitworld():
            oldclip = window.get_clip()
            window.set_clip(dare)
            for tx in [self.scrollpos[0]-world.surface.get_width(), self.scrollpos[0], self.scrollpos[0]+world.surface.get_width()]:
                tx += dare.left
                for ty in [self.scrollpos[1]-world.surface.get_height(), self.scrollpos[1], self.scrollpos[1]+world.surface.get_height()]:
                    ty += dare.top
                    if world.surface.get_rect(topleft=(tx, ty)).colliderect(dare):
                        window.blit(world.surface, (tx, ty))
            window.set_clip(oldclip)

        updatearea()
        updatescrollpos()
        blitworld()
        return self.scrollpos
