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

# ---------- BUTTONS ----------
start_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/start.png").convert_alpha(), (250, 100)
)
start_button_rect = start_button.get_rect(center=(400, 220))

howto_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/how to play.png").convert_alpha(), (250, 100)
)
howto_button_rect = howto_button.get_rect(center=(400, 320))

about_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/about.png").convert_alpha(), (250, 100)
)
about_button_rect = about_button.get_rect(center=(400, 420))

restart_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/restart 2.png").convert_alpha(), (100, 100)
)
restart_button_rect = restart_button.get_rect(topright=(800, 10))

pause_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/pause.png").convert_alpha(), (100, 100)
)
pause_button_rect = pause_button.get_rect(topright=(800, 10))

resume_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/resume.png").convert_alpha(), (200, 100)
)
resume_button_rect =    resume_button.get_rect(center=(400, 270))

back_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/back.png").convert_alpha(), (200, 100)
)
back_button_rect = back_button.get_rect(topleft=(0, 0))

menu_button = pygame.transform.scale(
    pygame.image.load("assets/buttons/menu.png").convert_alpha(), (200, 150)
)
menu_button_rect = menu_button.get_rect(topleft=(0, 0))
title= pygame.transform.scale(
    pygame.image.load("assets/buttons/riddler.png").convert_alpha(),(400,100)
)
title_rect= title.get_rect(center=(400,100))

# ---------- FUNCTIONS ----------
def reset_game():
    global lives, enemies, flying_enemies, current_riddle
    global start_time, collision_locked, show_feedback, game_state
    global riddles_answered, correct_answers, wrong_answers, end_time
    global player_rect, player_velocity, is_jumping, jump_frame, player_img

    lives = MAX_LIVES
    enemies.clear()
    flying_enemies.clear()
    current_riddle = 0
    riddles_answered = 0
    end_time = 0
    start_time = pygame.time.get_ticks()
    collision_locked = False
    show_feedback = False
    game_state = PLAYING
    correct_answers = 0
    wrong_answers = 0
    
    # Reset player
    player_rect = idle_img.get_rect(midbottom=(400, GROUND_LEVEL))
    player_velocity = 0
    is_jumping = False
    jump_frame = 0
    player_img = idle_img
# ---------- MAIN LOOP ----------
while True:
    # ---------- EVENT HANDLING ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ---------- KEYBOARD EVENTS ----------
        if event.type == pygame.KEYDOWN:
            # P key to pause/unpause
            if event.key == pygame.K_p:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING
            
            # Space key for jumping
            if game_state == PLAYING:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_velocity = JUMP_FORCE
                    is_jumping = True
                    jump_frame = 0
                    jump_sound.play()
            
            # Answer riddles with 1-4 keys
            if game_state == RIDDLE and not show_feedback:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    selected = event.key - pygame.K_1
                    correct = riddles[current_riddle]["answer"]
                    
                    riddles_answered += 1

                    if selected == correct:
                        feedback_text = "CORRECT!"
                        feedback_color = (0, 255, 0)
                        correct_sound.play()
                        correct_answers += 1
                    else:
                        feedback_text = "WRONG!"
                        feedback_color = (255, 0, 0)
                        lives -= 1
                        hit_sound.play()
                        wrong_answers += 1

                    show_feedback = True
                    feedback_start_time = pygame.time.get_ticks()
                    collision_locked = False
                    current_riddle += 1
# ---------- MOUSE EVENTS ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Menu buttons
            if game_state == MENU:
                if start_button_rect.collidepoint(mouse_pos):
                    reset_game()
                elif howto_button_rect.collidepoint(mouse_pos):
                    game_state = HOW_TO_PLAY
                elif about_button_rect.collidepoint(mouse_pos):
                    game_state = ABOUT
            
            # Pause/Resume buttons
            if game_state == PLAYING and pause_button_rect.collidepoint(mouse_pos):
                game_state = PAUSED
            
            if game_state == PAUSED and resume_button_rect.collidepoint(mouse_pos):
                game_state = PLAYING
            
            # Back button for multiple states
            if back_button_rect.collidepoint(mouse_pos):
                if game_state in (HOW_TO_PLAY, ABOUT, CONGRATS, PAUSED, RIDDLE):
                    game_state = MENU
            
            # Restart button
            if game_state == GAME_OVER and restart_button_rect.collidepoint(mouse_pos):
                reset_game()
        
        # ---------- ENEMY SPAWNING EVENTS ----------
        if event.type == ENEMY_EVENT and game_state == PLAYING and len(enemies) < 3:
            enemies.append(enemy_img.get_rect(midbottom=(random.randint(-150, -50), GROUND_LEVEL)))
        
        if event.type == FLYING_EVENT and game_state == PLAYING and len(flying_enemies) < 2:
            flying_enemies.append(
                flying_enemy_img.get_rect(midleft=(WIDTH + 50, random.randint(200, 320)))
            )

    # ---------- GAME LOGIC ----------
    if game_state == PLAYING:
        survival_time = (pygame.time.get_ticks() - start_time) // 1000

        # ---------- PLAYER PHYSICS ----------
        player_velocity += GRAVITY
        player_rect.y += player_velocity

        # Ground collision and animation
        if player_rect.bottom >= GROUND_LEVEL:
            player_rect.bottom = GROUND_LEVEL
            player_velocity = 0
            is_jumping = False
            jump_frame = 0
            player_img = idle_img
        else:
            is_jumping = True
            jump_frame += jump_anim_speed
            if jump_frame >= len(jump_img):
                jump_frame = len(jump_img) - 1
            player_img = jump_img[int(jump_frame)]
            

    pygame.display.update()
    
    pygame.time.Clock().tick(60)
