import pygame

class Player:
    def __init__(self, positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY
        self.speed = 100
        self.size = 16

    def drawPlayer(self, screen, image, cameraX, cameraY):
        screenX = self.positionX - cameraX
        screenY = self.positionY - cameraY
        screen.blit(image, (screenX, screenY))

    def updateLocation(self, moveX, moveY):
        self.positionX += moveX
        self.positionY += moveY

    def getCenter(self):
        return (self.positionX + self.size // 2, self.positionY + self.size // 2)
    