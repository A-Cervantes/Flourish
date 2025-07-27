import pygame
from mapDump import *
from Player import *
from Camera import *
from Plants import Plant
from Question import Question, level1_questions, level2_questions, level3_questions
import healthBar
import plantBar
import time
import sounds

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 32)

sounds.load_sounds()
sounds.play_music()

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
theStemFound = False

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
canAnswer = False
showHint = False
hintStartTime = None
hintDuration = 1000

# Game state variables
level_transition_active = False
transition_start_time = 0



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


def show_transition(screen, font, message1, message2):
    screen.fill((0, 0, 0))
    text1 = font.render(message1, True, (255, 255, 255))
    text2 = font.render(message2, True, (200, 200, 0))

    screen.blit(text1, (screen.get_width() // 2 - text1.get_width() // 2, 200))
    screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2, 250))

    pygame.display.update()
    pygame.time.delay(3000)



def handle_level_transition(nextLevel, nextMapFile, nextQuestion, mapWidth=800, mapHeight=600):
    global currentLevel, currentMap, mapCreation, player, currentQuestions, camera

    show_transition(screen, font,"Level Complete!", f"Moving to Level {nextLevel}...")
    pygame.time.delay(3000)

    currentLevel = nextLevel
    currentMap = nextMapFile

    # Load new map
    mapCreation = tileHandle(f"Visuals/Maps/{nextMapFile}.csv", nextMapFile)

    # Reset player
    player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
    player.plantsFullyGrowed = 0
    player.plantsQueue = []

    # Load new questions
    currentQuestions = nextQuestion

    # Reset camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, mapCreation.mapWidth, mapCreation.mapHeight)


while running:
    while introScreen:
        screen.fill((0, 105, 62)) 

        intro_lines = [
            "Welcome to Flourish!",
            "Press 'R' to start the game.",
            "Press 'E' to see your first question.",
            "Pick between 1–4 to answer correctly", 
            "and grow your sunflowers!"
        ]

        line_spacing = 35
        total_height = len(intro_lines) * line_spacing
        start_y = SCREEN_HEIGHT // 2 - total_height // 2

        for i, line in enumerate(intro_lines):
            rendered_text = font.render(line, True, (255, 253, 208))
            text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * line_spacing))
            screen.blit(rendered_text, text_rect)

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
                        player.tookDamage(3)
                        feedbackText = "Incorrect. Try again next time."
                        canPlant = False

                    showFeedback = True
                    pygame.time.set_timer(pygame.USEREVENT, 1500)

        if event.type == pygame.USEREVENT and showFeedback:
            if currentQuestion and currentQuestion.check_answer(userAnswer + 1):
                if canPlant:
                    player.addPoints(currentQuestion.points)
                    player.plantSeed(mapName, quiz_correct=True)
                questionIndex += 1
                if questionIndex >= len(questions):
                    #currentLevel += 1
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

        if player.onSecretRoot():
                theStemFound = True
                canAnswer = True
                if not sounds.secret_Stem_sound.get_num_channels():
                    sounds.secret_Stem_sound.play()


        # Quiz activation
        if keys[pygame.K_e] and not quizActive and mapName == "firstMap":
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
        elif keys[pygame.K_e] and not quizActive and mapName == "secondMap":
            if player.onSecretRoot():
                showHint = False
            
            if canAnswer:
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
            else:
                showHint = True
                hintStartTime = pygame.time.get_ticks()

                

        slowEffect = player.checkTileInteractions(mapName)

        # Player slow down logic
        if slowEffect:
            player.updateLocation(moveX * 0.5, moveY * 0.5, mapName)
            player.tookDamage(4 * deltaTime)
            if mapName == "firstMap":
                if direction == "right":
                    direction = "rightBush" 
                elif direction == "left":
                    direction = "leftBush"
                elif direction == "down":
                    direction = "downBush"
                elif direction == "up":
                    direction = "upBush"
            elif mapName == "secondMap":
                if direction == "right":
                    direction = "rightDarksand" 
                elif direction == "left":
                    direction = "leftDarksand"
                elif direction == "down":
                    direction = "downDarksand"
                elif direction == "up":
                    direction = "upDarksand"

        elif moving:
            player.updateLocation(moveX, moveY, mapName)
            if moving:
                if not pygame.mixer.Channel(1).get_busy():
                    pygame.mixer.Channel(1).play(sounds.walk_sound, loops=-1)
                    sounds.walk_sound.set_volume(0.3)
                else:
                    pygame.mixer.Channel(1).stop()



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
            plant.grow(deltaTime)

            currentGrowth = plant.getGrowthLevel()
            if plant.pastGrowthStage != currentGrowth:
                    player.updatePlant(plant.position[0], plant.position[1], currentGrowth, mapName)
                    plant.pastGrowthStage = currentGrowth

            if plant.is_fully_grown():
                justFullyGrown.append(plant) 
                player.plantsGrowed()
                
        # Health & Plant bar
        plantBarObj.update(len(justFullyGrown))
        plantBarObj.draw(screen)
        healthBarObj.draw(screen)

        player.plantsQueue = [plant for plant in player.plantsQueue if not plant.is_fully_grown()]


        if showHint:
            smallFont = pygame.font.SysFont("Arial", 16)

            invalidQuiz = "Find the Secret Stem to answer questions!"
            quizWarning = smallFont.render(invalidQuiz, True, (255, 0, 0))

            boxW = 400
            boxH = 80
            boxX = (SCREEN_WIDTH - boxW) // 2 + 25
            boxY = (SCREEN_HEIGHT - boxH) // 2  + 250 
            boxRect = pygame.Rect(boxX, boxY, boxW, boxH)

            pygame.draw.rect(screen, (40,40,40), boxRect)  # 
            pygame.draw.rect(screen, (100, 100, 100), boxRect, 3)  

            text_rect = quizWarning.get_rect(center=boxRect.center)
            screen.blit(quizWarning, text_rect)

            if pygame.time.get_ticks() - hintStartTime >= hintDuration:
                showHint = False

        if theStemFound:
            smallFont = pygame.font.SysFont("Arial", 18)

            invalidQuiz = "You fond the Secret Stem! "
            quizWarning = smallFont.render(invalidQuiz, True, (0, 255, 0))

            boxW = 400
            boxH = 80
            boxX = (SCREEN_WIDTH - boxW) // 2 + 25
            boxY = (SCREEN_HEIGHT - boxH) // 2  + 250 
            boxRect = pygame.Rect(boxX, boxY, boxW, boxH)

            pygame.draw.rect(screen, (40,40,40), boxRect)  # 
            pygame.draw.rect(screen, (100, 100, 100), boxRect, 3)  

            text_rect = quizWarning.get_rect(center=boxRect.center)
            screen.blit(quizWarning, text_rect)

            if pygame.time.get_ticks() - hintStartTime >= hintDuration:
                theStemFound = False



        # Quiz box
        if quizActive and currentQuestion:
            # Draw background quiz box
            pygame.draw.rect(screen, (30, 30, 30), (100, 100, 600, 450))
            pygame.draw.rect(screen, (200, 200, 200), (100, 100, 600, 450), 3)

            # Use the new method to render the question + choices
            currentQuestion.render(font, screen, start_y=120, max_width=550, selected_choice=userAnswer)

            # Feedback if needed
            if showFeedback:
                feedback_color = (0, 255, 0) if "Correct" in feedbackText else (255, 0, 0)
                feedback_surface = font.render(feedbackText, True, feedback_color)
                screen.blit(feedback_surface, (120, 500))

        
        # Game over check
        if player.gameOver(remainingTime):
            if not sounds.game_Over_sound.get_num_channels():
                sounds.game_Over_sound.play()
            game_over = True

        # if player.plantsFullyGrowed >= 3:
        #     levelWon = True
        #     screen.fill((0, 0, 0))
        #     mapName = "secondMap"
        #     mapCreation = tileHandle("Visuals/Maps/secondLevel.csv",mapName)
        #     player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
        #     endTime = time.time() + startTime
        #     healthBarObj = healthBar.healthBar(player)
        #     plantBarObj = plantBar.plantBar(len(player.plantsQueue))
        #     justFullyGrown = []
        #     currentLevel = 1
        #     questionIndex = 0
        #     quizActive = False
        #     currentQuestion = None
        #     userAnswer = None
        #     showFeedback = False
        #     feedbackText = ""
        #     canPlant = False
        #     game_over = False
        if player.plantsFullyGrowed >= 3 and not level_transition_active:
            if not sounds.level_Up_sound.get_num_channels():
                sounds.level_Up_sound.play()
            level_transition_active = True
            transition_start_time = pygame.time.get_ticks()

        


        if level_transition_active:
            elapsed = pygame.time.get_ticks() - transition_start_time
            if elapsed < 3000:
                if currentLevel == 1:
                    message = "Great job! Moving to Level 2..."
                elif currentLevel == 2:
                    message = "Awesome! Entering Level 3..."
                else:
                    message = "You're a Flourish expert!"
                show_transition(screen, font, "Level Complete!", message)

            elif elapsed >= 3000:
                # Only now increment the level and load the next
                if currentLevel == 1:
                    currentLevel = 2
                    mapName = "secondMap"
                    questions = level2_questions
                elif currentLevel == 2:
                    currentLevel = 3
                    mapName = "thirdMap"
                    questions = level3_questions
                else:
                    show_transition(screen, font, "You Win!", "Thanks for playing!")
                    pygame.time.delay(4000)
                    running = False
                    break  # or break if inside loop

                # Reload map and player
                mapCreation = tileHandle(f"Visuals/Maps/{mapName}.csv", mapName)
                player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y, PLAYER_HEALTH, mapCreation)
                camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, mapCreation.mapWidth, mapCreation.mapHeight)
                healthBarObj = healthBar.healthBar(player)
                plantBarObj = plantBar.plantBar(len(player.plantsQueue))
                justFullyGrown.clear()
                questionIndex = 0
                quizActive = False
                currentQuestion = None
                userAnswer = None
                showFeedback = False
                feedbackText = ""
                canPlant = False
                endTime = time.time() + startTime

                level_transition_active = False


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
    #Fpygame.mixer.music.stop() 