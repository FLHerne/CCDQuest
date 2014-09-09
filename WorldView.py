from images import BLOCKSIZE
import pygame

class WorldView:
    def __init__(self, world, area, window):
        self.area = pygame.Rect(area)
        self.dare = self.area.copy()
        self.scrollpos = [(-BLOCKSIZE*world.player.position[0])+self.area.width/2,
                          (-BLOCKSIZE*world.player.position[1])+self.area.height/2]
    
    def draw(self, world, window):
        def updatearea():
            self.dare.width = min(world.surface.get_width(), self.area.width)
            self.dare.height = min(world.surface.get_height(), self.area.height)
            self.dare.center = self.area.center

        def updatescrollpos():
            '''scroll towards the correct position'''
            for axis in [0, 1]:
                pq = (world.player.position[axis]*BLOCKSIZE+self.scrollpos[axis]) % world.surface.get_size()[axis]
                if world.surface.get_size()[axis] > 2*world.player.visibility*BLOCKSIZE:
                    dr = (world.player.visibility*BLOCKSIZE, self.dare.size[axis]-(world.player.visibility+1)*BLOCKSIZE)
                else:
                    dr = [self.dare.size[axis]/2]
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[-1],pq))-pq)/2) % world.surface.get_size()[axis]

        def blitworld():
            oldclip = window.get_clip()
            worldregion = self.dare
            window.set_clip(worldregion)
            for tx in [self.scrollpos[0]-world.surface.get_width(), self.scrollpos[0], self.scrollpos[0]+world.surface.get_width()]:
                tx += self.dare.left
                for ty in [self.scrollpos[1]-world.surface.get_height(), self.scrollpos[1], self.scrollpos[1]+world.surface.get_height()]:
                    ty += self.dare.top
                    if world.surface.get_rect(topleft=(tx, ty)).colliderect(worldregion):
                        window.blit(world.surface, (tx, ty))
            window.set_clip(oldclip)

        updatearea()
        updatescrollpos()
        blitworld()
        return self.scrollpos
