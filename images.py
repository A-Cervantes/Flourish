#Dictionary that holds images for easier access, for all 3 maps
#This is a global variable that can be accessed by other modules
def imageIndex():

    global imageVault
    global imageVault2
    global imageVault3
    global playerImage

    imageVault = {
        "bushGrass": "Visuals/Blocks/bushGrass.png", #Index 1
        "grass": "Visuals/Blocks/grass.png", #Index 2
        "treeTop": "Visuals/Blocks/treeTop.png", #Index 3
        "treeBottom": "Visuals/Blocks/treeBottom.png",# Index 4
        "seed": "Visuals/Blocks/seed.png", #Index 5
        "crabGrass": "Visuals/Blocks/crabGrass.png", #Index 6
        "sandBlock": "Visuals/Blocks/sandBlock.png", #Index 7
        "normalStem" : "Visuals/Blocks/normalStem.png",
        "sunFlower" : "Visuals/Blocks/sunFlower.png"
        }
    
    imageVault2 = {
        "Water": "Visuals/Blocks/water.png",
        "Stone": "Visuals/Blocks/stone.png",
        "darkSeed": "Visuals/Blocks/darkSeed.png",
        "theStem": "Visuals/Blocks/theStem.png",
        "darkGrass": "Visuals/Blocks/darkGrass.png",
        "darkSand": "Visuals/Blocks/darkSand.png",
        }

    imageVault3 = {}
    
imageIndex()