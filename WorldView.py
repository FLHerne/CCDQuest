from images import BLOCKSIZE
import pygame

class WorldView:
    def __init__(self, world, area, window):
        self.area = pygame.Rect(area)
        self.scrollpos = ((-BLOCKSIZE*world.player.position[0])+self.area.width/2,
                          (-BLOCKSIZE*world.player.position[1])+self.area.height/2)

    def draw(self, world, window):
        def updatescrollpos():
            '''scroll towards the correct position'''
            world.playerx = (world.player.position[0]*BLOCKSIZE + self.scrollpos[0]) % world.surface.get_width()
            world.playery = (world.player.position[1]*BLOCKSIZE + self.scrollpos[1]) % world.surface.get_height()
            print self.scrollpos[0], world.player.position[0], world.playerx, (world.player.visibility*BLOCKSIZE, self.area.width-world.player.visibility*BLOCKSIZE)
            if world.playerx+(world.player.visibility*BLOCKSIZE) > self.area.width:         #too far right
                scrollStep = (abs((world.playerx+(world.player.visibility*BLOCKSIZE)) - (self.area.width)) / 2) +1
                self.scrollpos = (self.scrollpos[0]-scrollStep, self.scrollpos[1])
            if world.playerx-(world.player.visibility*BLOCKSIZE) < 0:                         #too far left
                scrollStep = (abs((world.playerx-(world.player.visibility*BLOCKSIZE))) / 2) +1
                self.scrollpos = (self.scrollpos[0]+scrollStep, self.scrollpos[1])
            if world.playery+(world.player.visibility*BLOCKSIZE) > self.area.height:             #too far down
                scrollStep = (abs((world.playery+(world.player.visibility*BLOCKSIZE)) - self.area.height) / 2) +1
                self.scrollpos = (self.scrollpos[0], self.scrollpos[1]-scrollStep)
            if world.playery-(world.player.visibility*BLOCKSIZE) < 0:                         #too far up
                scrollStep = (abs((world.playery-(world.player.visibility*BLOCKSIZE))) / 2) +1
                self.scrollpos = (self.scrollpos[0], self.scrollpos[1]+scrollStep)
            self.scrollpos = (self.scrollpos[0] % world.surface.get_width(),
                              self.scrollpos[1] % world.surface.get_height())

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
