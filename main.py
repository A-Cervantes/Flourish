import pygame
from mapDump import *
from Player import *
from Camera import *
from Plants import Plant
from Question import Question, level1_questions, level2_questions, level3_questions
import healthBar
import time

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 32)

# Time control variables for movement
clock = pygame.time.Clock()
prevTime = time.time()

# Time control variables for game duration
startTime = 60
endTime = prevTime + startTime

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the display surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flourish Game")

# Sprite attributes 
PLAYER_SPEED = 100
PLAYER_HEALTH = 100
PLAYER_POSITION_X = 100
PLAYER_POSITION_Y = 100

# Game loop control variable
running = True

# Game state variables
game_over = False

# Quiz variables
current_level = 1
question_index = 0
quiz_active = False 
current_question = None
questions = []
user_answer = None  # Track which answer the player is selecting
show_feedback = False
feedback_text = ""

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

while running: 
    # Logic for calculating delta time
    currentTime = time.time()
    deltaTime = currentTime - prevTime
    prevTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle quiz input
        if not game_over and quiz_active and current_question:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    user_answer = 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    user_answer = 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    user_answer = 2
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    user_answer = 3
                elif event.key == pygame.K_RETURN and user_answer is not None:
                    if current_question.check_answer(user_answer + 1):
                        feedback_text = "Correct! You can plant a seed."
                        player.addPoints(current_question.points)
                        player.plantSeed(quiz_correct=True)
                        question_index += 1
                        show_feedback = True
                        # Level up if all questions are answered
                        if question_index >= len(questions):
                            current_level += 1
                            question_index = 0
                            feedback_text += f" Level up! Now at level {current_level}"
                    else:
                        feedback_text = "Incorrect. Try again next time."
                        show_feedback = True
                    # Move to next question after short delay
                    pygame.time.set_timer(pygame.USEREVENT, 1500)
            elif event.type == pygame.USEREVENT and show_feedback:
                show_feedback = False
                quiz_active = False
                current_question = None
                user_answer = None
                feedback_text = ""
                pygame.time.set_timer(pygame.USEREVENT, 0)

        # Handle game over restart
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Reset all game state variables
            player = Player(PLAYER_POSITION_X, PLAYER_POSITION_Y ,PLAYER_HEALTH, mapCreation)
            endTime = time.time() + startTime
            current_level = 1
            question_index = 0
            quiz_active = False
            current_question = None
            user_answer = None
            show_feedback = False
            feedback_text = ""
            game_over = False

    keys = pygame.key.get_pressed()
    moveX = 0
    moveY = 0

    if not game_over:
        if keys[pygame.K_w]:
            moveY = -PLAYER_SPEED * deltaTime
        if keys[pygame.K_s]:
            moveY = PLAYER_SPEED * deltaTime
        if keys[pygame.K_a]:
            moveX = -PLAYER_SPEED * deltaTime
        if keys[pygame.K_d]:
            moveX = PLAYER_SPEED * deltaTime 
        if keys[pygame.K_e] and not quiz_active:
            if current_level == 1:
                questions = level1_questions
            elif current_level == 2:
                questions = level2_questions
            else:
                questions = level3_questions

            if question_index < len(questions):
                current_question = questions[question_index]
                quiz_active = True
                user_answer = None
                show_feedback = False
                feedback_text = ""
            else:
                print("No more questions for this level.")
        
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

        # Logic for handling quiz questions when planting a seed
        if quiz_active and current_question:
            # Draw a background box for the quiz
            pygame.draw.rect(screen, (30, 30, 30), (100, 100, 600, 250))
            pygame.draw.rect(screen, (200, 200, 200), (100, 100, 600, 250), 3)

            # Render question text
            question_surface = font.render(current_question.question_text, True, (255, 255, 255))
            screen.blit(question_surface, (120, 120))

            # Render choices
            for idx, choice in enumerate(current_question.choices):
                color = (255, 255, 0) if user_answer == idx else (255, 255, 255)
                choice_surface = font.render(f"{idx+1}. {choice}", True, color)
                screen.blit(choice_surface, (140, 170 + idx * 40))

            # Show feedback if needed
            if show_feedback:
                feedback_surface = font.render(feedback_text, True, (0, 255, 0) if "Correct" in feedback_text else (255, 0, 0))
                screen.blit(feedback_surface, (120, 320)) 

        # Check for game over
        if player.gameOver(remainingTime):
            game_over = True

    else:
        # Game Over screen
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