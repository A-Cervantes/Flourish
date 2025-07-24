class Plant:
    def __init__(self, name, tileX=None, tileY=None):
        self.name = name
        self.growth_stage = 0  
        self.facts = []
        self.tileX = tileX  # Optional: track where the plant is on the map
        self.tileY = tileY

    def grow(self):
        if self.growth_stage < 3:
            self.growth_stage += 1
            print(f"{self.name} has grown to stage {self.growth_stage}!")
            # You can add logic here to update the plant's image on the map if needed
        else:
            print(f"{self.name} is fully grown!")

