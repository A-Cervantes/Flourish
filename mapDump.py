import csv
import pygame
from images import *

class mapDump(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale=1):
        super().__init__()
        original_image = pygame.image.load(image)
        if scale != 1:
            new_size = (original_image.get_width() * scale, original_image.get_height() * scale)
            self.image = pygame.transform.scale(original_image, new_size)
        else:
            self.image = original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, cameraX, cameraY):
        screenX = self.rect.x - cameraX
        screenY = self.rect.y - cameraY
        screen.blit(self.image, (screenX, screenY))

class tileHandle():
    def __init__(self, filename):
        self.filename = filename
        self.initX = 0
        self.initY = 0
        self.baseTileSize = 16  
        self.scale = 2  
        self.tileSize = self.baseTileSize * self.scale  
        self.tiles = self.tileDump(self.filename)
        self.numMap = self.readCSV(self.filename)
        
    def drawMap(self, screen, cameraX, cameraY, screenWidth, screenHeight):

        if self.tileGrid:
            tilesWide = len(self.tileGrid[0])
            tilesHigh = len(self.tileGrid)
        else:
            tilesWide = 0
            tilesHigh = 0

        startX = max(0, int(cameraX // self.tileSize) - 1)
        endX = min(tilesWide, int((cameraX + screenWidth) // self.tileSize) + 2)

        startY = max(0, int(cameraY // self.tileSize) - 1)
        endY = min(tilesHigh, int((cameraY + screenHeight) // self.tileSize) + 2)
        
        for y in range(startY, endY):
            for x in range(startX, endX):
                if self.tileGrid[y][x]: 
                    tile = self.tileGrid[y][x]
                    screenX = (x * self.tileSize) - cameraX
                    screenY = (y * self.tileSize) - cameraY
                    screen.blit(tile.image, (screenX, screenY))

    def readCSV(self, filename):
        mapArray = []
        try:
            with open(filename, newline='') as csvScan:
                csv_reader = csv.reader(csvScan, delimiter=',')
                for row in csv_reader:
                    mapArray.append(list(row))
            return mapArray
        except FileNotFoundError:
            print("Error with finding file!")
            return []
        
    def tileDump(self, filename):
        tiles = []
        mapArray = self.readCSV(filename)
        
        if not mapArray:
            return tiles
            
        # Create a 2D grid of "None", to replaces with tile blocks later 
        self.tileGrid = []
        for row in range (len(mapArray)):
            innerRow = []
            for col in range (len(mapArray[0])):
                innerRow.append(None);
            self.tileGrid.append(innerRow)
        
        y = 0
        for row in mapArray:
            x = 0
            for tileID in row:
                tileObject = None
                if tileID == '1':
                    tileObject = mapDump(imageVault["bushGrass"], x * self.tileSize, y * self.tileSize, self.scale)
                elif tileID == '2':
                    tileObject = mapDump(imageVault["grass"], x * self.tileSize, y * self.tileSize,  self.scale)
                elif tileID == '3':
                    tileObject = mapDump(imageVault["treeTop"], x * self.tileSize, y * self.tileSize,  self.scale)
                elif tileID == '4':
                    tileObject = mapDump(imageVault["treeBottom"], x * self.tileSize, y * self.tileSize, self.scale)
                elif tileID == '5':
                    tileObject = mapDump(imageVault["seed"], x * self.tileSize, y * self.tileSize,  self.scale)
                elif tileID == '6':
                    tileObject = mapDump(imageVault["crabGrass"], x * self.tileSize, y * self.tileSize,  self.scale)
                elif tileID == '7':
                    tileObject = mapDump(imageVault["sandBlock"], x * self.tileSize, y * self.tileSize,  self.scale)
                elif tileID == '0':
                    tileObject = mapDump(imageVault["biggrass"], x * self.tileSize, y * self.tileSize,  self.scale)
                
                #Load the image into the tileGrid array, so that it can displayed
                if tileObject:
                    tiles.append(tileObject)
                    self.tileGrid[y][x] = tileObject
                    
                x += 1
            y += 1

        # The dimensions of the map   
        self.mapWidth = x * self.tileSize
        self.mapHeight = y * self.tileSize
        return tiles