import pygame
import sys

pygame.init()

pygame.mixer.init()


# ---------- CONSTANTS ----------
WIDTH, HEIGHT = 800, 600
GROUND_LEVEL = 430
GRAVITY = 1
JUMP_FORCE = -22
MAX_LIVES = 3
RIDDLE_TIME = 30
FEEDBACK_DURATION = 1200

# ---------- STATES ----------
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
RIDDLE = "riddle"
GAME_OVER = "game over"
HOW_TO_PLAY = "how_to_play"
ABOUT = "about"
CONGRATS = "congrats"

game_state = MENU


screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("[RIDDLER]")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# ---------- ASSETS ----------
sky=pygame.transform.scale(pygame.image.load("assets/backgrounds/sky.jpeg"), (WIDTH, HEIGHT))
ground=pygame.transform.scale(pygame.image.load("assets/backgrounds/ground.jpeg"), (WIDTH, HEIGHT - GROUND_LEVEL))
menu_list=pygame.transform.scale(pygame.image.load("assets/backgrounds/menu background.jpeg"), (WIDTH, HEIGHT))
other_list=pygame.transform.scale(pygame.image.load("assets/backgrounds/listing.jpeg"), (WIDTH, HEIGHT))

#---------- ENEMIES ----------
enemy_img=pygame.image.load("assets/enemies/gary.jpeg").convert_alpha()
flying_enemy_img=pygame.image.load("assets/enemies/flying.jpeg").convert_alpha()
#---------- UI ELEMENTS ----------
heart_img=pygame.tranform.scale(
    pygame.image.load("assets/backgrounds/heart.jpeg").convert_alpha(), (32, 32)
)
congrats_message=pygame.transform.scale(
    pygame.image.load("assets/buttons/congratulations.jpeg").convert_alpha(), (400, 100)
)
congrats_message_rect=congrats_message.get_rect(center=(400,200))
game_over_message=pygame.transform.scale(
    pygame.image.load("assets/buttons/game over.jpeg").convert_alpha(), (250, 100)
)
game_over_message_rect=game_over_message.get_rect(center=(400,200))
#---------- SOUNDS ----------
jump_sound=pygame.mixer.Sound("assets/songs/jump.wav")
hit_sound=pygame.mixer.Sound("assets/songs/hit.wav")
correct_sound=pygame.mixer.Sound("assets/songs/correct.wav")
pygame.mixer.music.load("assets/songs/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    pygame.time.Clock().tick(60)
