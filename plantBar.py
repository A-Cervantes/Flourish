
import pygame

class plantBar():
    def __init__(self, plantsQueued):
        self.progress = plantsQueued
        self.width = 150
        self.height = 30
        self.x = 645
        self.y = 560

    def draw(self, screen):

        progressPercentage = self.progress / 3.0 #
        progressBarWidth = int(self.width * progressPercentage)

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(screen, (0, 105, 62), (self.x, self.y, progressBarWidth, self.height))

        progressText = f"Plants: {int(self.progress)}/3"
        visualBarText = pygame.font.Font(None, 24).render(progressText, True, (255, 222, 33))
        screen.blit(visualBarText, (self.x + 5, self.y + 5))

    def update(self, newProgress):
        self.progress = newProgress
    