import pygame
import csv
 
#Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game loop control variable
running = True

#Logic for creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flourish")

#Main loop 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Stop the game loop
    
    # Refreshes our game window to show the background color and all the drawn shapes
    pygame.display.flip()

# Clean up and close the window properly
pygame.quit()