class Plant:
    def __init__(self, name):
        self.name = name
        self.growth_stage = 0  # 0 = seed, 3 = full grown
        self.facts = []

    def grow(self):
        if self.growth_stage < 3:
            self.growth_stage += 1
            print(f"{self.name} has grown to stage {self.growth_stage}!")
        else:
            print(f"{self.name} is fully grown!")

    def addFact(self, fact):
        self.facts.append(fact)
