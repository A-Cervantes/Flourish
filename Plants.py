class Plant:
    def __init__(self, name, TileX, TileY):
        self.name = name
        self.growth_stage = 0  
        self.facts = []
        self.time = 0
        self.growthLevel = 0
        self.maxGrowth = 100  
        self.growthRate = 10  
        self.growthTimer = 0 
        self.TileX = TileX
        self.TileY = TileY
        self.position = (TileX, TileY)  
        self.pastGrowthStage = -1

    def grow(self, deltaTime):
        if self.growthLevel < self.maxGrowth:
            self.growthTimer += deltaTime

            if self.growthTimer >= 1.0:  
                self.growthLevel += self.growthRate
                self.growthTimer = 0 
                
                # Cap at maximum growth
                if self.growthLevel > self.maxGrowth:
                    self.growthLevel = self.maxGrowth
                    
                    

    
    def is_fully_grown(self):
        return self.growthLevel >= self.maxGrowth
    
    def halfWayGrown(self):
        return self.growthLevel == 50

    def setPosition(self, pos):
        self.position = pos
    
    def getPosition(self):
        return self.position

    def getGrowthLevel(self):
        return self.growthLevel

