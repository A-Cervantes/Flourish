import csv, os
import pygame

class mapDump(pygame.sprite.Sprite):
    def __init__(self,imagepath, x, y):
        super().__init__(self)
        self.imagepath = pygame.image.load(imagepath)
        self.rect = self.imagepath.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self, landscape):
        landscape.blit(self.imagepath, (self.rect.x, self.rect.y))


class tileHandle():
    def __init__(self,filename):
        self.filename = filename
        self.initX, self.initY = 0, 0
        self.tileSize = 16

    # Reads the CSV file and returns a 2D list of tiles
    def readCSV(self, filename):
        map = []
        with open(os.path.join(filename)) as csvScan:
            csvScan = csv.reader(csvScan, delimiter=',')
            for row in csvScan:
                map.append(list(row))
        return map
    
    def tileDump(self, filename):
        tiles = []
        map = self.readCSV(filename)
        y, x = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    x += self.tileSize
                    continue