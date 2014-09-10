import pygame
import images
import TextBox
import collectables
from colors import *

class HUD:
    def __init__(self, world, area, window):
        window.blit(images.HudImage, area)
        self.area = pygame.Rect(area)
        self.fontsize = 20
        self.miniWorld = pygame.transform.scale(world.surface, (90, (world.surface.get_height()/world.surface.get_width())*90))
    
    def draw(self, world, window, scrollpos):
        '''Draw the heads-up display, with current information'''
        window.blit(images.HudImage, (self.area))
        TextBox.Print(window,
                    False,      #Password
                    self.area.left+5, 75, #X, Y
                    100,        #Length
                    None,       #InColour
                    BLACK,      #FontColour
                    'Arial', self.fontsize,       #Font, Size
                    str(world.player.score[collectables.COIN]) + "/" + str(world.cellmap.origcoins),        #Message
                    True,       #Centre
                    [False, self.area.height])     #YCentre
        TextBox.Print(window,
                    False,
                    self.area.left+5, 275,
                    100,
                    None,
                    BLACK,
                    'Arial', self.fontsize,
                    str(world.player.score[collectables.DYNAMITE]),
                    True,
                    [False, self.area.height])
        if world.player.score[collectables.CHOCOLATE] >= 1000:
            ChocAmountString = str(round(world.player.score[collectables.CHOCOLATE] / 1000.0, 2)) + "kg"
        else:
            ChocAmountString = str(world.player.score[collectables.CHOCOLATE])+"g"
        TextBox.Print(window,
                    False,
                    self.area.left+5, 175,
                    100,
                    None,
                    BLACK,
                    'Arial', self.fontsize,
                    ChocAmountString,
                    True,
                    [False, self.area.height])
        old_clip = window.get_clip()
        window.set_clip((self.area.left+10, 302, 90, 90))
        pygame.transform.scale(world.surface, (90, (world.surface.get_height()/world.surface.get_width())*90), self.miniWorld)
        window.blit(self.miniWorld, (self.area.left+10, 302))
        miniWorldScale = 90.0/(world.cellmap.size[0]*images.BLOCKSIZE)
        for tx in [scrollpos[0]-world.surface.get_width(), scrollpos[0], scrollpos[0]+world.surface.get_width()]:
            for ty in [scrollpos[1]-world.surface.get_height(), scrollpos[1], scrollpos[1]+world.surface.get_height()]:
                pygame.draw.rect(window,
                    world.player.color,
                    ((self.area.left+10)-(tx*miniWorldScale), # Top x corner of minimap, plus scroll offset
                    302-                (ty*miniWorldScale), # Top y ''
                    1+ self.area.left*miniWorldScale,
                    1+ self.area.height*miniWorldScale),
                    1)
        window.set_clip(old_clip)
    
    def endsplash(self, reason, window):
        def splash(message):
            TextBox.Print(window, False,
                          0, 0, window.get_width(),
                          BLACK, WHITE, 'Arial', self.fontsize*2,
                          message,
                          True, [True, window.get_height()])
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
