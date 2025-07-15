import pygame

class Player:
    def __init__(self, positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY
        self.speed = 0.5
        self.resize = 16
     

    def drawPlayer(self, screen, image):
        screen.blit(image,(self.positionX * self.resize, self.positionY * self.resize))

    def updateLocation(self,moveX, moveY):
        self.positionX += moveX * self.speed
        self.positionY += moveY * self.speed
        print("This is the X postition " + str(self.positionX) + " " + " and this is the Y position " + str(self.positionY))

        

    

    