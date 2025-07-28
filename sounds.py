import pygame

# Placeholder for sound variables
secret_Stem_sound = None
level_Up_sound = None
game_Over_sound = None
walk_sound = None


def load_sounds():
    global secret_Stem_sound, level_Up_sound, game_Over_sound, walk_sound

    # Load short sound effects
    secret_Stem_sound = pygame.mixer.Sound('soundFiles/secret_Stem.wav')
    level_Up_sound = pygame.mixer.Sound('soundFiles/level_Up.wav')
    game_Over_sound = pygame.mixer.Sound('soundFiles/game_Over.wav')
    walk_sound = pygame.mixer.Sound('soundFiles/chick_Walking.wav')  
    print("Sounds loaded successfully")
    walk_sound.set_volume(1.0)  # Try 1.0 first for max volume

def play_music():
    # Use mixer.music for long background music
    pygame.mixer.music.load('soundFiles/bg_music.wav')  
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop forever
    print("Playing music...")
