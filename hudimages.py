import pygame

'''Load and convert all HUD images'''

# HUD score widget images.
Coin = pygame.image.load("hud/MoneyBag.png").convert_alpha()
Choc = pygame.image.load("hud/ChocolateBar.png").convert_alpha()
Dynamite = pygame.image.load("hud/Dynamite.png").convert_alpha()

# HUD frame and background textures.
FrameHoriz =  pygame.image.load("hud/WoodenRuleHoriz.png").convert_alpha()
FrameVert =  pygame.image.load("hud/WoodenRule.png").convert()
HudBackground = pygame.image.load("hud/RockWall.png").convert()

# MessageBox background textures.
MessageBackground = pygame.image.load("hud/MessageBackground.png").convert()
MessageBackgroundLeft = pygame.image.load("hud/MessageBackgroundLeft.png").convert()
MessageBackgroundRight = pygame.image.load("hud/MessageBackgroundRight.png").convert()
