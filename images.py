import pygame
import collectables

'''this file loads the images needed for CCDQuest, and converts them if necessary'''
BLOCKSIZE = 8

Unknown = pygame.image.load("tiles/Unknown.png")           # Used for tiles that must appear to be empty blank nothingness
NonVisible = pygame.image.load("tiles/NonVisible.png")     # An overlay for no-longer-visible tiles

Damage = pygame.image.load("tiles/Damage.png")             # An overlay for damaged (blown-up) tiles
Damage = Damage.convert_alpha()                            # this image is transparent, so the alpha must be used too

Coin = pygame.image.load("tiles/Coin.png")                 # images for collectables
Coin = Coin.convert_alpha()                                # collectables have transparent backgrounds
Choc = pygame.image.load("tiles/Chocolate.png")
Choc = Choc.convert_alpha()
Dynamite = pygame.image.load("tiles/Dynamite.png")
Dynamite = Dynamite.convert_alpha()

Water = pygame.image.load("tiles/Water.png")               # images for terrain
DeepWater = pygame.image.load("tiles/DeepWater.png")
Rock = pygame.image.load("tiles/Rock.png")
Paving = pygame.image.load("tiles/Paving.png")
Grass = pygame.image.load("tiles/Grass.png")
Marsh = pygame.image.load("tiles/Marsh.png")
Wall = pygame.image.load("tiles/Wall.png")
Glass = pygame.image.load("tiles/Glass.png")
Wood = pygame.image.load("tiles/Wood.png")
Trees = pygame.image.load("tiles/Trees.png")
Sand = pygame.image.load("tiles/Sand.png")
Snow = pygame.image.load("tiles/Snow.png")

BearLeft = pygame.image.load("tiles/Bear.png")
BearRight = pygame.transform.flip(BearLeft, True, False)

CollectablesImages = {
    collectables.COIN: Coin,                           # semi-enum for referencing collectable images
    collectables.CHOCOLATE: Choc,
    collectables.DYNAMITE: Dynamite
}