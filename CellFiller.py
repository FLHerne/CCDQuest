from colors import *
import collectables

terraint = {
    # name top destructable temperature fireignitechance fireoutchance hasroof difficulty transparent solid
    BLACK:
        ('wall', False, True, 20, 0, 1, False, 3, False, True),
    GREY:
        ('rocky ground', False, True, 20, 0, 1, False, 5, True, False),
    BROWN:
        ('wooden planking', False, True, 20, 0.4, 0.1, False, 2, True, False),
    WHITE:
        ('snow', False, True, -5, 0, 1, False, 4, True, False),
    LIGHTBLUE:
        ('water', False, False, 12, 0, 1, False, 25, True, False),
    BLUE:
        ('deep water', False, False, 8, 0, 1, False, 25, True, True),
    GREEN:
        ('grass', False, True, 20, 0.1, 0.3, False, 2, True, False),
    BLUEGREY:
        ('marshland', False, True, 20, 0, 1, False, 20, True, False),
    CYAN:
        ('window', False, True, 20, 0, 1, False, 3, True, True),
    DARKGREEN:
        ('forest', True, True, 20, 0.5, 0.1, False, 8, False, False),
    DARKYELLOW:
        ('sand', False, True, 20, 0, 1, False, 3, True, False),
    LIGHTYELLOW:
        ('paving', False, True, 20, 0, 1, False, 1, True, False),
    DARKPINK:
        ('floor', False, True, 20, 0.5, 0.05, True, 1, True, False)
}

collectablet = {
    WHITE: (0,),
    MAGENTA: (0,),
    YELLOW: (collectables.COIN,),
    BROWN: (collectables.CHOCOLATE,),
    RED: (collectables.DYNAMITE,)
}
