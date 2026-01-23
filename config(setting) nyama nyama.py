import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
FPS = 60

BG_COLOR = (120, 85, 50)
PANEL_COLOR = (70, 40, 20)
TEXT_COLOR = (255, 240, 200)
BAR_BG = (60, 30, 15)
BAR_FG = (200, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyama Nyama")

clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arialblack", 46)
font_mid = pygame.font.SysFont("arial", 26)
font_small = pygame.font.SysFont("arial", 20)