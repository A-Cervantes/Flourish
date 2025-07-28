#Dictionary that holds images for easier access, for all 3 maps
#This is a global variable that can be accessed by other modules
def imageIndex():

    global imageVault
    global imageVault2
    global imageVault3
    global sunFlowerVault
    global sunFlowerVaultDark

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

    imageVault3 = {
        "darkGrass": "Visuals/Blocks/darkGrass.png",
        "darkSand": "Visuals/Blocks/darkSand.png",
        "theStem": "Visuals/Blocks/theStem.png",
        "water": "Visuals/Blocks/water.png",
        "stone": "Visuals/Blocks/stone.png",
        "normalStem" : "Visuals/Blocks/normalStem.png",
        "sunFlower" : "Visuals/Blocks/sunFlower.png"
    }

    sunFlowerVault = {
        "sunFlower1": "Visuals/Blocks/sunFlower1.png",
        "sunFlower2": "Visuals/Blocks/sunFlower2.png",
        "sunFlower3": "Visuals/Blocks/sunFlower3.png",
        "sunFlower4": "Visuals/Blocks/sunFlower4.png",
        "sunFlower5": "Visuals/Blocks/sunFlower5.png",
        "sunFlower6": "Visuals/Blocks/sunFlower6.png",
        "sunFlower7": "Visuals/Blocks/sunFlower7.png",
        "sunFlower8": "Visuals/Blocks/sunFlower8.png",
        "sunFlower9": "Visuals/Blocks/sunFlower9.png",
        "sunFlower10": "Visuals/Blocks/sunFlower10.png"
    }
    sunFlowerVaultDark = {
        "sunFlowerDark1": "Visuals/Blocks/sunFlowerDark1.png",
        "sunFlowerDark2": "Visuals/Blocks/sunFlowerDark2.png",
        "sunFlowerDark3": "Visuals/Blocks/sunFlowerDark3.png",
        "sunFlowerDark4": "Visuals/Blocks/sunFlowerDark4.png",
        "sunFlowerDark5": "Visuals/Blocks/sunFlowerDark5.png",
        "sunFlowerDark6": "Visuals/Blocks/sunFlowerDark6.png",
        "sunFlowerDark7": "Visuals/Blocks/sunFlowerDark7.png",
        "sunFlowerDark8": "Visuals/Blocks/sunFlowerDark8.png",
        "sunFlowerDark9": "Visuals/Blocks/sunFlowerDark9.png",
        "sunFlowerDark10": "Visuals/Blocks/sunFlowerDark10.png"
    }
    
imageIndex()