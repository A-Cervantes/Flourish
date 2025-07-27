import pygame

# Initialize sounds (don't call mixer.init() here — do that once in main)
jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')

#function to play background music
def play_music():
    pygame.mixer.music.load('assets/sounds/music.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop forever
