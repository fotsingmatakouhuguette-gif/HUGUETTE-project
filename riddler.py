import pygame
import sys

pygame.init()
WIDTH,HEIGHT=800,600

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("[RIDDLER]")

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    pygame.time.Clock().tick(60)
