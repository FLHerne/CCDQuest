import pygame
import images
import TextBox
import collectables
from colours import *

class HUD:
    def __init__(self, area, window, world):
        window.blit(images.HudImage, area)
        self.area = pygame.Rect(area)
        self.fontsize = 20
        self.miniWorld = pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90))
    
    def draw(self, player, window, world, scrollpos, cellmap):
        '''Draw the heads-up display, with current information'''
        window.blit(images.HudImage, (self.area))
#Print(window,Password = False, X = 500, Y = 200, Length = 200, InColour = (255,255,255),FontColour = (0,0,0), Font = None, Size = 48, Message = '', Centre = False, YCentre = [False,200], PrintLength = False)
        TextBox.Print(window,
                    False,      #Password
                    self.area.left+5, 75, #X, Y
                    100,        #Length
                    None,       #InColour
                    BLACK,      #FontColour
                    'Arial', self.fontsize,       #Font, Size
                    str(player.score[collectables.COIN]) + "/" + str(cellmap.origcoins),        #Message
                    True,       #Centre
                    [False, self.area.height])     #YCentre
        TextBox.Print(window,
                    False,
                    self.area.left+5, 275,
                    100,
                    None,
                    BLACK,
                    'Arial', self.fontsize,
                    str(player.score[collectables.DYNAMITE]),
                    True,
                    [False, self.area.height])
        if player.score[collectables.CHOCOLATE] >= 1000:
            ChocAmountString = str(round(player.score[collectables.CHOCOLATE] / 1000.0, 2)) + "kg"
        else:
            ChocAmountString = str(player.score[collectables.CHOCOLATE])+"g"
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
        pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90), self.miniWorld)
        window.blit(self.miniWorld, (self.area.left+10, 302))
        miniWorldScale = 90.0/(cellmap.size[0]*images.BLOCKSIZE)
        for tx in [scrollpos[0]-world.get_width(), scrollpos[0], scrollpos[0]+world.get_width()]:
            for ty in [scrollpos[1]-world.get_height(), scrollpos[1], scrollpos[1]+world.get_height()]:
                pygame.draw.rect(window,
                    player.color,
                    ((self.area.left+10)-(tx*miniWorldScale), # Top x corner of minimap, plus scroll offset
                    302-                (ty*miniWorldScale), # Top y ''
                    1+ self.area.left*miniWorldScale,
                    1+ self.area.height*miniWorldScale),
                    1)
        window.set_clip(old_clip)