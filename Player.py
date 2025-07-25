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
        self.knowledgePoints = 0
        self.gardenSlots = 1
        self.seedsCollected = 1000;
        self.plants = [] 
        self.completed_tasks = []
        self.unlocked_facts = []
        self.plantsQueue = []
        self.plantsFullyGrowed = 0

        self.bushGrass = '1'
        self.grass = '2'
        self.treeTop = '3'
        self.treeBottom = '4'
        self.seed = '5'
        self.crabGrass = '6'
        self.sandBlock = '7'

        directions = {
            "right": ["birdRight+1.png", "birdRight+2.png", "birdRight+3.png"],
            "left": ["birdLeft+1.png", "birdLeft+2.png", "birdLeft+2.png"],
            "up": ["bird.png", "bird_right.png"],
            "down": ["birdDown+1.png", "birdDown+2.png", "birdDown+3.png", "birdDown+4.png"],
            "right_bush": ["birdRightBush+1.png", "birdRightBush+2.png", "birdRightBush+3.png"],
            "left_bush": ["birdLeftBush+1.png", "birdLeftBush+2.png", "birdLeftBush+3.png"],
        }

        self.animations = {}
        for direction, files in directions.items():
            self.animations[direction] = [pygame.image.load(f"Visuals/Sprites/{filename}") for filename in files]

        self.currentFrame = 0
        self.animationTimer = 0
        self.animationSpeed = 0.4
        self.direction = "right"  

    def updateAnimation(self, deltaTime, moving):
        if moving:
            self.animationTimer += deltaTime
            if self.animationTimer >= self.animationSpeed:
                self.animationTimer = 0
                self.currentFrame = (self.currentFrame + 1) % len(self.animations[self.direction])
        else:
            self.currentFrame = 0  

        if self.currentFrame >= len(self.animations[self.direction]):
            self.currentFrame = 0

    def drawPlayer(self, screen, cameraX, cameraY):
        screenX = self.positionX - cameraX
        screenY = self.positionY - cameraY
        image = self.animations[self.direction][self.currentFrame]
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


    #Need to add logic for other maps, add canMoveTo the world as paramerter
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
        if len(self.plants) < self.gardenSlots:
            self.plants.append(plant)
        else:
            print("Garden full! Level up to grow more plants.")


    def levelUp(self):
        self.level += 1
        self.gardenSlots += 1
        print(f"Leveled up to {self.level}! You can now grow {self.gardenSlots} plants.")

    def displayStats(self):
        print(f"Level: {self.level}")
        print(f"Knowledge Points: {self.knowledgePoints}")
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
        self.knowledgePoints += points
        print(f"Knowledge Points increased by {points}. Total: {self.knowledgePoints}")
    
    def plantSeed(self, quiz_correct=False):
        if not quiz_correct:
            return False

        if self.plantQueueFull():
            return False

        if self.seedsCollected > 0:
            # Get the current tile we are on
            centerX, centerY = self.getCenter()
            tileX = int(centerX // self.tileSize)
            tileY = int(centerY // self.tileSize)
            
            if self.tileMap[tileY][tileX] != self.grass:
                print("You cannot plant here :{")
                return False
            else:
                print("You can plant here!")
                if self.addToPlantQueue(tileX, tileY):
                    self.tileMap[tileY][tileX] = self.seed
                    
                    newTile = mapDump(imageVault["seed"], tileX * self.tileSize, tileY * self.tileSize, self.tileHandler.scale)
                    self.tileHandler.tileGrid[tileY][tileX] = newTile
                    
                    self.seedsCollected -= 1
                    print(f"Added plant to queue. Queue size: {len(self.plantsQueue)}")
                    for plant in self.plantsQueue:
                        print(plant.getPosition())

                    return True
                else:
                    print("Failed to add to plant queue")
                    return False
        
        print("No seeds available!")
        return False

    def gameOver(self, remainingTime):
        return not self.isAlive() or remainingTime <= 0
    
    def plantQueueFull(self):
        return len(self.plantsQueue) >= 3

    def addToPlantQueue(self, tileX, tileY):
        if len(self.plantsQueue) < 3:
            self.plantsQueue.append((Plant("Sunflower", tileX, tileY)))
            return True
        return False
    
    def plantsGrowed(self, tileX, tileY):
        self.plantsFullyGrowed += 1
        newTile = mapDump(imageVault["sunFlower"], tileX * self.tileSize, tileY * self.tileSize, self.tileHandler.scale)
        self.tileHandler.tileGrid[tileY][tileX] = newTile

    def plantHalfGrown(self, tileX, tileY):
        newTile = mapDump(imageVault["normalStem"], tileX * self.tileSize, tileY * self.tileSize, self.tileHandler.scale)
        
        self.tileHandler.tileGrid[tileY][tileX] = newTile
        