import pygame

class Camera:
    def __init__(self, screenWidth, screenHeight, mapWidth, mapHeight):
        self.cameraX = 0
        self.cameraY = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.smoothing = 0.7 
        
    def update(self, targetX, targetY):

        lockX = targetX - self.screenWidth // 2
        lockY = targetY - self.screenHeight // 2
        
        # linear interpolation for a smooth looking camera
        self.cameraX += (lockX - self.cameraX) * self.smoothing
        self.cameraY += (lockY - self.cameraY) * self.smoothing
        
        #Boundcamera for keeping camera in view of the world
        self.cameraX = max(0, min(self.cameraX, self.mapWidth - self.screenWidth))
        self.cameraY = max(0, min(self.cameraY, self.mapHeight - self.screenHeight))