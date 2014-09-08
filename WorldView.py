from images import BLOCKSIZE
import pygame

class WorldView:
    def __init__(self, world, area, window):
        self.area = pygame.Rect(area)
        self.scrollpos = [(-BLOCKSIZE*world.player.position[0])+self.area.width/2,
                          (-BLOCKSIZE*world.player.position[1])+self.area.height/2]

    def draw(self, world, window):
        def updatescrollpos():
            '''scroll towards the correct position'''
            for axis in [0, 1]:
                pq = (world.player.position[axis]*BLOCKSIZE+self.scrollpos[axis]) % world.surface.get_size()[axis]
                dr = (world.player.visibility*BLOCKSIZE, self.area.size[axis]-world.player.visibility*BLOCKSIZE)
                self.scrollpos[axis] = (self.scrollpos[axis]+(max(dr[0],min(dr[1],pq))-pq)/2) % world.surface.get_size()[axis]

        def blitworld():
            oldclip = window.get_clip()
            worldregion = self.area
            window.set_clip(worldregion)
            for tx in [self.scrollpos[0]-world.surface.get_width(), self.scrollpos[0], self.scrollpos[0]+world.surface.get_width()]:
                for ty in [self.scrollpos[1]-world.surface.get_height(), self.scrollpos[1], self.scrollpos[1]+world.surface.get_height()]:
                    if world.surface.get_rect(topleft=(tx, ty)).colliderect(worldregion):
                        window.blit(world.surface, (tx, ty))
            window.set_clip(oldclip)

        updatescrollpos()
        blitworld()
        return self.scrollpos
