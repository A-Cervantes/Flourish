import pygame
from mapDump import *
from Player import *
from Camera import *
from Plants import Plant
from Question import Question, level1_questions, level2_questions, level3_questions
import healthBar
import plantBar
import time

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 32)

# Time control variables
clock = pygame.time.Clock()
prevTime = time.time()
startTime = 180
endTime = prevTime + startTime

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the display surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flourish Game")

# Sprite attributes 
PLAYER_SPEED = 80
PLAYER_HEALTH = 100
PLAYER_POSITION_X = 100
PLAYER_POSITION_Y = 100

# Game loop control variables
running = True
playAgain = False
introScreen = True
game_over = False
levelWon = False
justFullyGrown = []
mapName = "firstMap"

# Quiz variables
currentLevel = 1
questionIndex = 0
quizActive = False 
currentQuestion = None
questions = []
userAnswer = None
showFeedback = False
feedbackText = ""
canPlant = False 

# Initialize game objects
mapCreation = tileHandle("Visuals/Maps/mainMap.csv", mapName)
player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, mapCreation.mapWidth, mapCreation.mapHeight)
healthBarObj = healthBar.healthBar(player)
plantBarObj = plantBar.plantBar(len(player.plantsQueue))

try:
    playerImage = pygame.image.load("Visuals/Sprites/bird_right.png")
except pygame.error:
    print("Image not found!")
    pygame.quit()

while running:
    while introScreen:
        screen.fill((0, 105, 62))
        instructions = [
            "Welcome to Flourish!",
            "Press 'R' to start.",
            "Press E to view your first question.",
            "Pick between numbers 1-4 to answer!"
        ]
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, (255, 253, 208))
            # Adjust the position as needed for centering and spacing
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                introScreen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                introScreen = False
                prevTime = time.time()
                endTime = prevTime + startTime

    # Delta time calculation
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime
    moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Quiz input
        if not game_over and quizActive and currentQuestion:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    userAnswer = 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    userAnswer = 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    userAnswer = 2
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    userAnswer = 3
                elif event.key == pygame.K_RETURN and userAnswer is not None:

                    if currentQuestion.check_answer(userAnswer + 1):
                        if player.plantQueueFull():
                            feedbackText = "Queue is full! Can't plant more seeds."
                            canPlant = False
                        else:
                            feedbackText = "Correct! You can plant a seed."
                            canPlant = True
                    else:
                        feedbackText = "Incorrect. Try again next time."
                        canPlant = False

                    showFeedback = True
                    pygame.time.set_timer(pygame.USEREVENT, 1500)

        if event.type == pygame.USEREVENT and showFeedback:
            if currentQuestion and currentQuestion.check_answer(userAnswer + 1):
                if canPlant:
                    player.addPoints(currentQuestion.points)
                    player.plantSeed(quiz_correct=True)
                questionIndex += 1
                if questionIndex >= len(questions):
                    currentLevel += 1
                    questionIndex = 0
            
            # Reset quiz state
            showFeedback = False
            quizActive = False
            currentQuestion = None
            userAnswer = None
            feedbackText = ""
            canPlant = False
            pygame.time.set_timer(pygame.USEREVENT, 0)

        # Game over logic
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            screen.fill((0, 0, 0))
            mapCreation = tileHandle("Visuals/Maps/mainMap.csv", mapName)
            player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
            endTime = time.time() + startTime
            healthBarObj = healthBar.healthBar(player)
            plantBarObj = plantBar.plantBar(len(player.plantsQueue))
            print(str(len(player.plantsQueue)) + "This is the amount of plants that are in this ")
            justFullyGrown = []
            print(len(justFullyGrown))
            currentLevel = 1
            questionIndex = 0
            quizActive = False
            currentQuestion = None
            userAnswer = None
            showFeedback = False
            feedbackText = ""
            canPlant = False
            game_over = False
            

    keys = pygame.key.get_pressed()
    moveX = 0
    moveY = 0
    direction = 'right'
    slowEffect = False

    if not game_over:
        if keys[pygame.K_w]:
            moveY = -PLAYER_SPEED * deltaTime
            moving = True
            direction = 'up'
        if keys[pygame.K_s]:
            moveY = PLAYER_SPEED * deltaTime
            moving = True
            direction = 'down'
        if keys[pygame.K_a]:
            moveX = -PLAYER_SPEED * deltaTime
            moving = True
            direction = 'left'
        if keys[pygame.K_d]:
            moveX = PLAYER_SPEED * deltaTime
            moving = True
            direction = 'right'

        # Quiz activation
        if keys[pygame.K_e] and not quizActive:
            if currentLevel == 1:
                questions = level1_questions
            elif currentLevel == 2:
                questions = level2_questions
            else:
                questions = level3_questions

            if questionIndex < len(questions):
                currentQuestion = questions[questionIndex]
                quizActive = True
                userAnswer = None
                showFeedback = False
                feedbackText = ""
                canPlant = False
            else:
                print("No more questions for this level.")

        slowEffect = player.checkTileInteractions()

        # Player slow down logic
        if slowEffect:
            player.updateLocation(moveX * 0.5, moveY * 0.5)
            player.tookDamage(8 * deltaTime)
            if direction == "right":
                direction = "right_bush" 
            elif direction == "left":
                 direction = "left_bush"
            elif direction == "down":
                direction = "down_bush"
            elif direction == "up":
                print("I am going up")
                direction = "up_bush"
        elif moving:
            player.updateLocation(moveX, moveY)


        #Making sure questions align with levels
        if player.plantsFullyGrowed >= 3:
            levelWon = True
            screen.fill((0, 0, 0))
            mapName = "secondMap"
            mapCreation = tileHandle("Visuals/Maps/secondLevel.csv", mapName)
            player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
            endTime = time.time() + startTime
            healthBarObj = healthBar.healthBar(player)
            plantBarObj = plantBar.plantBar(len(player.plantsQueue))
            justFullyGrown = []
            currentLevel = 2  # <-- Set to the next level!
            questionIndex = 0
            # Set questions for the new level
            if currentLevel == 1:
                questions = level1_questions
            elif currentLevel == 2:
                questions = level2_questions
            else:
                questions = level3_questions
            quizActive = False
            currentQuestion = None
            userAnswer = None
            showFeedback = False
            feedbackText = ""
            canPlant = False
            game_over = False


        # Keep player inside map
        player.positionX = max(0, min(player.positionX, mapCreation.mapWidth - player.size))
        player.positionY = max(0, min(player.positionY, mapCreation.mapHeight - player.size))

        player.direction = direction
        
        player.updateAnimation(deltaTime, moving)

        # Camera update
        playerCenter = player.getCenter()
        camera.update(playerCenter[0], playerCenter[1])

        # Drawing
        mapCreation.drawMap(screen, camera.cameraX, camera.cameraY, SCREEN_WIDTH, SCREEN_HEIGHT)
        player.drawPlayer(screen, camera.cameraX, camera.cameraY)

        # Timer
        remainingTime = max(0, int(endTime - time.time()))
        minutes = remainingTime // 60
        seconds = remainingTime % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        timerArt = font.render(timer_text, True, (255, 253, 208))
        screen.blit(timerArt, (SCREEN_WIDTH - 120, 20))

    
        for plant in player.plantsQueue:
            print(plant.getPosition())
            plant.grow(deltaTime)

            if plant.halfWayGrown():
                    player.plantHalfGrown(plant.position[0], plant.position[1])
            
            if plant.is_fully_grown():
                justFullyGrown.append(plant) 
                print("A plant is grown I WILL ADD ONE TO YOUR SCORE")
                player.plantsGrowed(plant.position[0], plant.position[1])
                
        # Health & Plant bar
        plantBarObj.update(len(justFullyGrown))
        plantBarObj.draw(screen)
        healthBarObj.draw(screen)

        player.plantsQueue = [plant for plant in player.plantsQueue if not plant.is_fully_grown()]

        # Quiz box
        if quizActive and currentQuestion:
            pygame.draw.rect(screen, (30, 30, 30), (100, 100, 600, 250))
            pygame.draw.rect(screen, (200, 200, 200), (100, 100, 600, 250), 3)
            question_surface = font.render(currentQuestion.question_text, True, (255, 255, 255))
            screen.blit(question_surface, (120, 120))
            for idx, choice in enumerate(currentQuestion.choices):
                color = (255, 255, 0) if userAnswer == idx else (255, 255, 255)
                choice_surface = font.render(f"{idx+1}. {choice}", True, color)
                screen.blit(choice_surface, (140, 170 + idx * 40))
            if showFeedback:
                feedback_surface = font.render(
                    feedbackText,
                    True,
                    (0, 255, 0) if "Correct" in feedbackText else (255, 0, 0)
                )
                screen.blit(feedback_surface, (120, 320))


        # Game over check
        if player.gameOver(remainingTime):
            game_over = True

        if player.plantsFullyGrowed >= 3:
            levelWon = True
            screen.fill((0, 0, 0))
            mapName = "secondMap"
            mapCreation = tileHandle("Visuals/Maps/secondLevel.csv",mapName)
            player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
            endTime = time.time() + startTime
            healthBarObj = healthBar.healthBar(player)
            plantBarObj = plantBar.plantBar(len(player.plantsQueue))
            justFullyGrown = []
            currentLevel = 1
            questionIndex = 0
            quizActive = False
            currentQuestion = None
            userAnswer = None
            showFeedback = False
            feedbackText = ""
            canPlant = False
            game_over = False

    else:
        try:
            fancyFont = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
        except:
            fancyFont = font
        gameOverText = fancyFont.render("Game Over!", True, (255, 253, 208))
        gameOverText2 = fancyFont.render("Press 'Space' to play again", True, (255, 253, 208))
        screen.fill((0, 0, 0))
        screen.blit(gameOverText, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 80))
        screen.blit(gameOverText2, (SCREEN_WIDTH // 2 - 340, SCREEN_HEIGHT // 2 - 10))

    pygame.display.flip()