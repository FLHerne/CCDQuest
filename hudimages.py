import pygame

'''Load and convert all HUD images'''

# HUD score widget images.
HudCoin = pygame.image.load("hud/MoneyBag.png").convert_alpha()
HudChoc = pygame.image.load("hud/ChocolateBar.png").convert_alpha()
HudDynamite = pygame.image.load("hud/Dynamite.png").convert_alpha()

# HUD frame and background textures.
HudFrameHoriz =  pygame.image.load("hud/WoodenRuleHoriz.png").convert()
HudFrameVert =  pygame.image.load("hud/WoodenRule.png").convert()
HudBackground = pygame.image.load("hud/RockWall.png").convert()

# MessageBox background textures.
HudMessageBackground = pygame.image.load("hud/MessageBackground.png").convert()
HudMessageBackgroundLeft = pygame.image.load("hud/MessageBackgroundLeft.png").convert()
HudMessageBackgroundRight = pygame.image.load("hud/MessageBackgroundRight.png").convert()
