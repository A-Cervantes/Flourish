# Player.py
import pygame

class Player:
    def __init__(self, positionX, positionY):
        # Movement & rendering
        self.positionX = positionX
        self.positionY = positionY
        self.speed = 100
        self.size = 16

        # Game logic
        self.level = 1
        self.knowledge_points = 0
        self.garden_slots = 1
        self.plants = []  # list of Plant objects
        self.completed_tasks = []
        self.unlocked_facts = []

    # --- Movement & Drawing ---
    def drawPlayer(self, screen, image, cameraX, cameraY):
        screenX = self.positionX - cameraX
        screenY = self.positionY - cameraY
        screen.blit(image, (screenX, screenY))

    def updateLocation(self, moveX, moveY):
        self.positionX += moveX
        self.positionY += moveY

    def getCenter(self):
        return (self.positionX + self.size // 2, self.positionY + self.size // 2)

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

    