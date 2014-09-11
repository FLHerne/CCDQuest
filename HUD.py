import pygame
import images
import TextBox
import newTextBox
import collectables
from colors import *

class HUD:
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.miniWorld = pygame.transform.scale(world.surface, (90, (world.surface.get_height()/world.surface.get_width())*90))
    
    def draw(self, area, scrollpos):
        '''Draw the heads-up display, with current information'''
        area = pygame.Rect(area)
        self.window.blit(images.HudImage, (area))
        
        # Score indicators
        if self.world.player.score[collectables.CHOCOLATE] >= 1000:
            ChocAmountString = str(round(self.world.player.score[collectables.CHOCOLATE] / 1000.0, 2)) + "kg"
        else:
            ChocAmountString = str(self.world.player.score[collectables.CHOCOLATE])+"g"
        def scoretext(y, text):
            TextBox.Print(self.window, False,
                          area.left+5, y, 100,
                          None, BLACK, 'Arial', 20,
                          text,
                          True, [False, area.height])
        scoretext(75, str(self.world.player.score[collectables.COIN]) + "/" + str(self.world.cellmap.origcoins))
        scoretext(175, ChocAmountString)
        scoretext(275, str(self.world.player.score[collectables.DYNAMITE]))

        # Minimap
        old_clip = self.window.get_clip()
        self.window.set_clip((area.left+10, 302, 90, 90))
        pygame.transform.scale(self.world.surface, (90, (self.world.surface.get_height()/self.world.surface.get_width())*90), self.miniWorld)
        self.window.blit(self.miniWorld, (area.left+10, 302))
        miniWorldScale = 90.0/(self.world.cellmap.size[0]*images.BLOCKSIZE)
        for tx in [scrollpos[0]-self.world.surface.get_width(), scrollpos[0], scrollpos[0]+self.world.surface.get_width()]:
            for ty in [scrollpos[1]-self.world.surface.get_height(), scrollpos[1], scrollpos[1]+self.world.surface.get_height()]:
                pygame.draw.rect(self.window,
                    self.world.player.color,
                    ((area.left+10)-(tx*miniWorldScale), # Top x corner of minimap, plus scroll offset
                    302-                (ty*miniWorldScale), # Top y ''
                    1+ area.left*miniWorldScale,
                    1+ area.height*miniWorldScale),
                    1)
        self.window.set_clip(old_clip)
    
    def endsplash(self, reason):
        '''Display a splash message across the entire window'''
        def splash(message):
            TextBox.Print(self.window, False,
                          0, 0, self.window.get_width(),
                          BLACK, WHITE, 'Arial', 40,
                          message,
                          True, [True, self.window.get_height()])
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
