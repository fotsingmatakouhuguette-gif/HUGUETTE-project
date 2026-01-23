import pygame
import json
import random
from sys import exit
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

# ---------- LOAD RIDDLES ----------
with open("riddles.json", "r", encoding="utf-8") as f:
    riddles = json.load(f)

current_riddle = 0
riddles_answered = 0
end_time = 0
correct_answers = 0
wrong_answers = 0
best_time = 0

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

# ---------- PLAYER SPRITES ---------
idle_img = pygame.image.load("assets/player/saut/idle.png").convert_alpha()
jump_img = [
    pygame.image.load(f"assets/player/saut/jump_{i}.png").convert_alpha()
    for i in range(4)
]

player_img = idle_img
player_rect = player_img.get_rect(midbottom=(400, GROUND_LEVEL))
player_velocity = 0
is_jumping = False
jump_frame = 0
jump_anim_speed = 0.2

#---------- ENEMIES ----------
enemy_img=pygame.image.load("assets/enemies/gary.jpeg").convert_alpha()
flying_enemy_img=pygame.image.load("assets/enemies/flying.png").convert_alpha()
#---------- UI ELEMENTS ----------
heart_img=pygame.transform.scale(
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
correct_sound=pygame.mixer.Sound("assets/songs/jump.wav")
pygame.mixer.music.load("assets/songs/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

 #---------- GAME DATA ----------
lives = MAX_LIVES
start_time = pygame.time.get_ticks()
survival_time = 0
riddle_start_time = 0
collision_locked = False

feedback_text = ""
feedback_color = (255, 255, 255)
feedback_start_time = 0
show_feedback = False

# ---------- ENEMIES LIST ----------
enemies = []
flying_enemies = []

ENEMY_EVENT = pygame.USEREVENT + 1
FLYING_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_EVENT, 2000)
pygame.time.set_timer(FLYING_EVENT, 3000)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    
    pygame.time.Clock().tick(60)
