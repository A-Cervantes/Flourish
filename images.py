import pygame 

#Dictionary that holds images for easier access
#This is a global variable that can be accessed by other modules

imageVault = {}

def imageIndex():

    global imageVault

    imageVault = {
            "bushGrass": "Visuals/Blocks/bushGrass.png", #Index 1
            "grass": "Visuals/Blocks/grass.png", #Index 2
            "treeTop": "Visuals/Blocks/treeTop.png", #Index 3
            "treeBottom": "Visuals/Blocks/treeBottom.png",# Index 4
            "seed": "Visuals/Blocks/seed.png", #Index 5
            "crabGrass": "Visuals/Blocks/crabGrass.png", #Index 6
            "sandBlock": "Visuals/Blocks/sandBlock.png" #Index 7
        }

imageIndex()