from colors import *
import collectables

terraint = {
    # name top destructable temperature fireignitechance fireoutchance hasroof difficulty transparent solid
    BLACK:
        ('wall', False, True, 20, 0, 1, False, 3, False, True, 7),
    GREY:
        ('rocky ground', False, True, 20, 0, 1, False, 5, True, False, 2),
    BROWN:
        ('wooden planking', False, True, 20, 0.4, 0.1, False, 2, True, False, 9),
    WHITE:
        ('snow', False, True, -5, 0, 1, False, 4, True, False, 12),
    LIGHTBLUE:
        ('water', False, False, 12, 0, 1, False, 25, True, False, 0),
    BLUE:
        ('deep water', False, False, 8, 0, 1, False, 25, True, True, 1),
    GREEN:
        ('grass', False, True, 20, 0.1, 0.3, False, 2, True, False, 5),
    BLUEGREY:
        ('marshland', False, True, 20, 0, 1, False, 20, True, False, 6),
    CYAN:
        ('window', False, True, 20, 0, 1, False, 3, True, True, 8),
    DARKGREEN:
        ('forest', True, True, 20, 0.5, 0.1, False, 8, False, False, 10),
    DARKYELLOW:
        ('sand', False, True, 20, 0, 1, False, 3, True, False, 11),
    LIGHTYELLOW:
        ('paving', False, True, 20, 0, 1, False, 1, True, False, 3),
    DARKPINK:
        ('floor', False, True, 20, 0.5, 0.05, True, 1, True, False, 4)
}

collectablet = {
    WHITE: (0,),
    MAGENTA: (0,),
    YELLOW: (collectables.COIN,),
    BROWN: (collectables.CHOCOLATE,),
    RED: (collectables.DYNAMITE,)
}
