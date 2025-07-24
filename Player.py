import pygame
from mapDump import *
from Plants import Plant

class Player:
    def __init__(self, positionX, positionY, initialHealth, tileHandler):
        self.positionX = positionX
        self.positionY = positionY
        self.speed = 100
        self.size = 32
        self.hitboxSize = 1  
        self.health = initialHealth

        self.tileHandler = tileHandler        
        self.tileMap = tileHandler.numMap
        self.tileSize = tileHandler.tileSize

        self.level = 1
        self.knowledge_points = 0
        self.garden_slots = 1
        self.seedsCollected = 1000;
        self.plants = [] 
        self.completed_tasks = []
        self.unlocked_facts = []

        self.bushGrass = '1'
        self.grass = '2'
        self.treeTop = '3'
        self.treeBottom = '4'
        self.seed = '5'
        self.crabGrass = '6'
        self.sandBlock = '7'

    # --- Movement & Drawing ---
    def drawPlayer(self, screen, image, cameraX, cameraY):
        screenX = self.positionX - cameraX
        screenY = self.positionY - cameraY
        screen.blit(image, (screenX, screenY))

    def updateLocation(self, moveX, moveY):
        oldX = self.positionX
        oldY = self.positionY
        
        newX = self.positionX + moveX
        newY = self.positionY + moveY
        
        if self.canMoveTo(newX, newY):
            self.positionX = newX
            self.positionY = newY

        elif self.canMoveTo(newX, oldY):
            self.positionX = newX

        elif self.canMoveTo(oldX, newY):
            self.positionY = newY


    def canMoveTo(self, x, y):

        walkableTiles = [self.bushGrass,self.grass,self.seed,self.crabGrass,self.sandBlock]  
        solidTiles = [self.treeTop, self.treeBottom] 
        
        hitboxOffset = (self.size - self.hitboxSize) // 2

        # Math for the corners for the sprite
        corners = [
            (x + hitboxOffset, y + hitboxOffset),  
            (x + hitboxOffset + self.hitboxSize - 1, y + hitboxOffset), 
            (x + hitboxOffset, y + hitboxOffset + self.hitboxSize - 1),  
            (x + hitboxOffset + self.hitboxSize - 1, y + hitboxOffset + self.hitboxSize - 1)  
        ]
        
        for cornerX, cornerY in corners:
            tileX = int(cornerX // self.tileSize)
            tileY = int(cornerY // self.tileSize)
            
            if (tileX < 0 or tileY < 0 or 
                tileY >= len(self.tileMap) or 
                tileX >= len(self.tileMap[0])):
                return False
            
            currentTile = self.tileMap[tileY][tileX]
            if currentTile in solidTiles:
                return False
        
        return True

    def getCenter(self):
        return (self.positionX + self.size // 2, self.positionY + self.size // 2)

    def getCurrentTile(self):
        centerX, centerY = self.getCenter()
        tileX = int(centerX // self.tileSize)
        tileY = int(centerY // self.tileSize)
        
        if (tileX < 0 or tileY < 0 or 
            tileY >= len(self.tileMap) or 
            tileX >= len(self.tileMap[0])):
            return None
        
        return self.tileMap[tileY][tileX]

    # --- Game Logic ---
    def addPlant(self, plant):
        if len(self.plants) < self.garden_slots:
            self.plants.append(plant)
        else:
            print("Garden full! Level up to grow more plants.")


    def levelUp(self):
        self.level += 1
        self.garden_slots += 1
        print(f"Leveled up to {self.level}! You can now grow {self.garden_slots} plants.")

    def displayStats(self):
        print(f"Level: {self.level}")
        print(f"Knowledge Points: {self.knowledge_points}")
        print(f"Plants Growing: {[p.name for p in self.plants]}")
        print(f"Tasks Completed: {[t.name for t in self.completed_tasks]}")
        print(f"Facts Unlocked: {len(self.unlocked_facts)}")
    
    def isAlive(self):
        return self.health > 0  
        
    def tookDamage(self, damage):
        self.health -= damage  

    def gainHealth(self, health):
        self.health += health  
   
    def checkTileInteractions(self):
        currentTile = self.getCurrentTile()
        return currentTile == self.bushGrass or currentTile == self.crabGrass
    
    def addPoints(self, points):
        self.knowledge_points += points
        print(f"Knowledge Points increased by {points}. Total: {self.knowledge_points}")
    
    def plantSeed(self, quiz_correct=False):
        if not quiz_correct:
            print("You must answer a question correctly to plant a seed!")
            return

        if self.seedsCollected > 0:
            # Get the current tile we are on
            centerX, centerY = self.getCenter()
            tileX = int(centerX // self.tileSize)
            tileY = int(centerY // self.tileSize)
            
            if self.tileMap[tileY][tileX] != self.grass:
                print("You cannot plant here :{")
            else:
                print("You can plant here!")
                self.tileMap[tileY][tileX] = self.seed
            
                # Update that tile with a seed image
                newTile = mapDump(imageVault["seed"], tileX * self.tileSize, tileY * self.tileSize, self.tileHandler.scale)
                self.tileHandler.tileGrid[tileY][tileX] = newTile
                
                self.seedsCollected -= 1

    def gameOver(self, remainingTime):
        return not self.isAlive() or remainingTime <= 0