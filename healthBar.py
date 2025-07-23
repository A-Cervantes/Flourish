import pygame

class healthBar():
    def __init__(self, player):
        self.player = player
        self.width = 200
        self.height = 30
        self.x = 10
        self.y = 560

    def draw(self, screen):
        healthPercentage = self.player.health / 100.0
        healthBarWidth = int(self.width * healthPercentage)

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(screen, (0, 105, 62), (self.x, self.y, healthBarWidth, self.height))

        healthText = f"Health: {int(self.player.health)}"
        visualHealthText = pygame.font.Font(None, 24).render(healthText, True, (255, 222, 33))
        screen.blit(visualHealthText, (self.x + 5, self.y + 5))