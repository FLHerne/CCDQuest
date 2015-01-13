CCDQuest
========

A grid-based adventure game featuring coins, chocolate and dynamite

Aims:
-----------
* Collect coins
* Collect chocolate
* Collect dynamite
* Avoid bears
* Avoid dragons

Basic concepts:
-----------
* Dynamite can be used to destroy obstacles, but not in water
* Each tile requires you to eat some chocolate - more for more difficult tiles
* Dragons and fire make you lose chocolate
* Bears make you lose coins, some of which are scattered around
* You must not run out of chocolate

Settings:
-----------
All settings are in CCDQuest.cfg and described there

Map content:
-----------
* Terrain types are specified in map/terrain.csv
    - r,g,b: Representing color in maps' terrain images
    - destr: Destructable with dynamite
    - ignite: Probability of igniting each turn if a neighbour is burning
    - out: Probability of fire going out each turn
    - solid: Terrain is a solid block of something (e.g walls)
    - temp: Temerature, in vague degrees-C
    - trans: Transparent
    - covered: Has a roof or similar (not necessarily shown)
    - soggy/roughness: Sogginess and roughness, as percentages
    - ground/topimage: Sprite(s) to use below and above player
        - Refer to subdirectories of tiles/terrain/
        - Square PNG images are used as-is, 6:1 (W:H) images represent sets of neighbour-sensitive sprites (see wall for example)
        - Each tile's sprite is randomly selected from images in tiles/terrain/<name>/, or only from neighbour-sensitive sets if one or more is present
        - Sprites are centred on their tile and must have side length below 2x TILESIZE
        - Large tile sprites overlap in the same order as their entries in terrain.csv
        - Magenta (#FF00FF) is used for transparency

* Maps each have a directory under map/, which must contain a file <dirname>.json
This file is in JSON format, with the following attributes:
    - "name": Required. Name of the map as seen by players
    - "terrainfile": Required. PNG file in the map directory representing terrain types from map/terrain.csv
    - "itemfile": Required. PNG file with location of coins (#FFFF00), chocolate (#7F4000) and dynamite (#FF0000)
    - "startpos": Required. Initial position [x, y] of a player not arriving by portal.
    - "gemgos": Optional. Positions and properties of in-game objects, with optional subattributes:
        - "signs": List of positions and text of signs [[x, y], text]
        - "portals": List of positions and destination of portals [[x, y], destmap, [dx, dy]]. 'destmap' must have a portal at (dx, dy).
        - "pixies": List of initial positions and strings of pixies [[x, y], [string1, string2, stringn]]

Notes:
-----------
* This is a target application for FLHerne's [mapgen](https://github.com/FLHerne/mapgen)
