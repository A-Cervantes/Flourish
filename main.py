import pygame
import csv
from mapDump import *
from Player import *
import time

#Initialize Pygame
pygame.init()

#time control variables
clock = pygame.time.Clock()
prevTime = time.time()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Sprite movements
PLAYER_SPEED = 10

# Game loop control variable
running = True

#Logic for creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flourish")

#Initalize game objects to be able to us
map = tileHandle("Visuals/Maps/worldMap.csv") # Load the map from a CSV file
initPlayer = Player(0,0)
playerImage = pygame.image.load("Visuals/Sprites/testSprite.png")

while running: 
    #Logic for calculatind delta time
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Stop the game loop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        initPlayer.updateLocation(0, -PLAYER_SPEED * deltaTime)
    if keys[pygame.K_a]:
        initPlayer.updateLocation(-PLAYER_SPEED * deltaTime, 0)
    if keys[pygame.K_s]:
        initPlayer.updateLocation(0, PLAYER_SPEED * deltaTime)
    if keys[pygame.K_d]:
        initPlayer.updateLocation(PLAYER_SPEED * deltaTime, 0)

    # Refreshes our game window and also redraws sprites that move dynamically
    map.drawMap(screen)
    initPlayer.drawPlayer(screen, playerImage)
    pygame.display.flip()
    clock.tick(60)

# Clean up and close the window properly
pygame.quit()