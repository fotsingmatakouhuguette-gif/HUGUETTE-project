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

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    pygame.time.Clock().tick(60)
