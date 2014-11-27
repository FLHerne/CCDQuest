import os.path
import pygame

"""Load and convert all HUD images"""

def pathimage(*path, **kwargs):
    convfunc = pygame.Surface.convert_alpha if ('alpha' in kwargs and kwargs['alpha']) else pygame.Surface.convert
    return convfunc(pygame.image.load(os.path.join(*path)))

# HUD score widget images.
Coin = pathimage('hud', 'MoneyBag.png', alpha=True)
Choc = pathimage('hud', 'ChocolateBar.png', alpha=True)
Dynamite = pathimage('hud', 'Dynamite.png', alpha=True)

# HUD frame and background textures.
FrameHoriz =  pathimage('hud', 'WoodenRuleHoriz.png', alpha=True)
FrameVert =  pathimage('hud', 'WoodenRule.png')
HudBackground = pathimage('hud', 'RockWall.png')

# MessageBox background textures.
MessageBackground = pathimage('hud', 'MessageBackground.png')
MessageBackgroundLeft = pathimage('hud', 'MessageBackgroundLeft.png')
MessageBackgroundRight = pathimage('hud', 'MessageBackgroundRight.png')

HourGlass = pathimage('hud', 'HourGlass.png', alpha=True)
