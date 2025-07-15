import pygame
from mapDump import *
from Player import *
from Camera import *
import time

# Initialize Pygame
pygame.init()

# Time control variables
clock = pygame.time.Clock()
prevTime = time.time()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Sprite movements
PLAYER_SPEED = 100

# Game loop control variable
running = True

# Logic for creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flourish")

# Initialize game objects
mapCreation = tileHandle("Visuals/Maps/worldMap.csv")
player = Player(100, 100) 
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, mapCreation.mapWidth, mapCreation.mapHeight)

try:
    playerImage = pygame.image.load("Visuals/Sprites/testSprite.png")
except pygame.error:
    print("Image not found!")

while running: 
    # Logic for calculating delta time
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player movement
    keys = pygame.key.get_pressed()
    moveX = 0
    moveY = 0
    
    if keys[pygame.K_w]:
        moveY = -PLAYER_SPEED * deltaTime
    if keys[pygame.K_s]:
        moveY = PLAYER_SPEED * deltaTime
    if keys[pygame.K_a]:
        moveX = -PLAYER_SPEED * deltaTime
    if keys[pygame.K_d]:
        moveX = PLAYER_SPEED * deltaTime

    player.updateLocation(moveX, moveY)

    # Keep the player sprite inside the world map; same logic as camera
    player.positionX = max(0, min(player.positionX, mapCreation.mapWidth - player.size))
    player.positionY = max(0, min(player.positionY, mapCreation.mapHeight - player.size))
    
    # Update camera to follow player by following its "hitbox"
    playerCenter = player.getCenter()
    camera.update(playerCenter[0], playerCenter[1])
    
    screen.fill((0, 0, 0))
    
    mapCreation.drawMap(screen, camera.cameraX, camera.cameraY, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    player.drawPlayer(screen, playerImage, camera.cameraX, camera.cameraY)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()