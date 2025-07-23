import pygame
from mapDump import *
from Player import *
from Camera import *
from Plants import Plant
from Tasks import Task
import healthBar
import time

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 32)

# Time control variables for movement
clock = pygame.time.Clock()
prevTime = time.time()

#Time control variables for game duration
startTime = 60
endTime = prevTime + startTime

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Sprite attributes 
PLAYER_SPEED = 100
PLAYER_HEALTH = 100
PLAYER_POSITION_X = 100
PLAYER_POSITION_Y = 100

# Game loop control variable
running = True
playAgain = False

# Logic for creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 50)
pygame.display.set_caption("Flourish")

# Initialize game objects
mapCreation = tileHandle("Visuals/Maps/mainMap.csv")
player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y ,PLAYER_HEALTH, mapCreation) 
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, mapCreation.mapWidth, mapCreation.mapHeight)
healthBar = healthBar.healthBar(player)

try:
    playerImage = pygame.image.load("Visuals/Sprites/bird.png")
except pygame.error:
    print("Image not found!")
    pygame.quit()

# Sample data
testPlant = Plant("Sunflower")
testTask = Task("Water the plant", "Find the watering can and use it.", points=2)

player.addPlant(testPlant)
player.current_tasks = [testTask]

while running: 
    # Logic for calculating delta time
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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
    if keys[pygame.K_SPACE]:
        if player.current_tasks:
            current_task = player.current_tasks[0]
            player.completeTask(current_task)
            testPlant.grow()
    if keys[pygame.K_e]:
        player.plantSeed();
    
    slowEffect = player.checkTileInteractions()

    if(slowEffect):
        player.updateLocation(moveX * 0.5, moveY * 0.5)
        player.tookDamage(2 * deltaTime) 
    else:
         player.updateLocation(moveX, moveY)


    # Keep the player sprite inside the world map; same logic as camera
    player.positionX = max(0, min(player.positionX, mapCreation.mapWidth - player.size))
    player.positionY = max(0, min(player.positionY, mapCreation.mapHeight - player.size))
    
    # Update camera to follow player by following its "hitbox"
    playerCenter = player.getCenter()
    camera.update(playerCenter[0], playerCenter[1])
    
    mapCreation.drawMap(screen, camera.cameraX, camera.cameraY, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    player.drawPlayer(screen, playerImage, camera.cameraX, camera.cameraY)
    
    remainingTime = max(0, int(endTime - time.time()))
    minutes = remainingTime // 60
    seconds = remainingTime % 60
    timer_text = f"{minutes:02}:{seconds:02}"

    timerArt = font.render(timer_text, True, (255, 253, 208))
    screen.blit(timerArt, (SCREEN_WIDTH - 120, 20)) 

    healthBar.draw(screen)

    if player.gameOver(remainingTime):
        print(remainingTime)
        print("GAME OVER!")
        try:
            fancyFont = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
        except:
            fancyFont = font  

        gameOverText = fancyFont.render("Game Over!", True, (255, 253, 208))
        gameOverText2 = fancyFont.render("Press 'Space' to play again", True, (255, 253, 208))
        text_rect = gameOverText.get_rect(center=(400, 300))
        screen.fill((0, 0, 0)) 
        screen.blit(gameOverText, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 80))
        screen.blit(gameOverText2, (SCREEN_WIDTH // 2 - 340, SCREEN_HEIGHT // 2 - 10))

        if(keys[pygame.K_SPACE] and not playAgain):
            playAgain = True

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()