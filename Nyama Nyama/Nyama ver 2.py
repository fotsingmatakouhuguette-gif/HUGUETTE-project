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
#-------------------------ASSETS----------------------------
#image=pygame.transform.scale(pygame.image.load("Nyama Nyama/assets/menu_back.jpeg"),(WIDTH,HEIGHT))
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

def load_high_score():
    if not os.path.exists(HS_FILE):
        with open(HS_FILE, "w") as f:
            f.write("0")
    with open(HS_FILE, "r") as f:
        return int(f.read())

def save_high_score(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

def load_categories():
    categories = []
    try:
        with open("categories.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(",")
                    if len(parts) >= 2:
                        category_name = parts[0].strip()
                        words = [word.strip() for word in parts[1:]]
                        
                        # Determine if category is "NOT" category (false) or regular category (true)
                        is_true = not category_name.upper().startswith("NOT ")
                        
                        categories.append((category_name, words, is_true))
    except FileNotFoundError:
        print("Error: categories.txt not found!")
        # Fallback to basic categories if file not found
        categories = [
            ("EDIBLE FOOD", ["Fish", "Chicken"], True),
            ("NOT EDIBLE", ["Rock", "Plastic"], False)
        ]
    return categories

categories = load_categories()