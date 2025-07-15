import csv
import pygame
from images import *

class mapDump(pygame.sprite.Sprite):
    def __init__(self,image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class tileHandle():
    def __init__(self, filename,):
        self.filename = filename
        self.initX, self.initY = 0, 0
        self.tileSize = 16
        self.tiles = self.tileDump(self.filename)
        self.mapSurface= pygame.Surface((self.mapWidth, self.mapHeight))
        self.mapSurface.set_colorkey((0, 0, 0))  
        self.mapStore()
    
    def mapStore(self):
        for tile in self.tiles:
            tile.draw(self.mapSurface)

    def drawMap(self, screen):
        screen.blit(self.mapSurface, (0,0))

    # Reads the CSV file and returns a 2D list of tiles
    def readCSV(self, filename):
        map = []
        try:
            with open(filename, newline='') as csvScan:
                csv_reader = csv.reader(csvScan, delimiter=',')
                for row in csv_reader:
                    map.append(list(row))
            return map
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            return []
        
    
    def tileDump(self, filename):
        tiles = []
        map = self.readCSV(filename)
        y, x = 0, 0
 
        for row in map:
            x = 0
            for tile in row:
                if tile == '1':
                    tiles.append(mapDump(imageVault["bushGrass"], x * self.tileSize, y * self.tileSize))
                elif tile == '2':
                    tiles.append(mapDump(imageVault["grass"], x * self.tileSize, y * self.tileSize))
                elif tile == '3':
                    tiles.append(mapDump(imageVault["treeTop"], x * self.tileSize, y * self.tileSize))
                elif tile == '4':
                    tiles.append(mapDump(imageVault["treeBottom"], x * self.tileSize, y * self.tileSize))
                elif tile == '5':
                    tiles.append(mapDump(imageVault["seed"], x * self.tileSize, y * self.tileSize))
                elif tile == '6':
                    tiles.append(mapDump(imageVault["crabGrass"], x * self.tileSize, y * self.tileSize))
                elif tile == '7':
                    tiles.append(mapDump(imageVault["sandBlock"], x * self.tileSize, y * self.tileSize))
                else:
                    print("Invalid block")
                x += 1
            y += 1

        #Log the dimensions of the map   
        self.mapWidth = x * self.tileSize
        self.mapHeight = y * self.tileSize
        return tiles


