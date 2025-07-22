import pygame
from mapDump import *

class Player:
    def __init__(self, positionX, positionY, initialHealth):
        self.positionX = positionX
        self.positionY = positionY
        self.speed = 100
        self.size = 32
        self.hitboxSize = 1  
        self.health = initialHealth
        
        self.tileHandler = tileHandle("Visuals/Maps/worldMap.csv")
        self.tileMap = self.tileHandler.numMap
        self.tileSize = self.tileHandler.tileSize

        self.level = 1
        self.knowledge_points = 0
        self.garden_slots = 1
        self.plants = [] 
        self.completed_tasks = []
        self.unlocked_facts = []

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
        walkableTiles = ['0', '1', '2', '5', '6']  
        solidTiles = ['3', '4', '7'] 
        
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

    def completeTask(self, task):
        if task not in self.completed_tasks:
            self.completed_tasks.append(task)
            self.knowledge_points += task.points
            print(f"Task '{task.name}' completed! Gained {task.points} knowledge points.")

    def unlockFact(self, fact):
        if fact not in self.unlocked_facts:
            self.unlocked_facts.append(fact)
            self.knowledge_points += 1
            print(f"Unlocked new fact: {fact}")

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
        
        if currentTile == '5':  # Seed tile
            print("Found a seed!")

        elif currentTile == '7':  # Sand block
            print("Standing on sand - maybe slower movement?")
       