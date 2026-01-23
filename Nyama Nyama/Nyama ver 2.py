import pygame
import random
import sys
import time
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyama Nyama Game")

clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arialblack", 46)
FONT_MED = pygame.font.SysFont("arial", 26)
FONT_SMALL = pygame.font.SysFont("arial", 20)

BG_COLOR = (25, 25, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (200, 70, 70)
GREEN = (70, 200, 120)
BLUE = (70, 130, 180)
PURPLE = (147, 112, 219)
BOX_COLOR = (45, 45, 55)
SELECTED_BOX_COLOR = (70, 70, 80)

HS_FILE = "highscore.txt"