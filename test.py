# COMPLETE NYAMA NYAMA GAME WITH SOUNDS - CORRECTED VERSION
import pygame
import random
import sys
import os
import math  # Added math module

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nyama Nyama Game - With Sounds!")
clock = pygame.time.Clock()

# Load sounds (create 'sounds' folder with WAV files)
try:
    jump_sound = pygame.mixer.Sound("sounds/jump.wav")
    shout_sound = pygame.mixer.Sound("sounds/shout.wav")
    correct_sound = pygame.mixer.Sound("sounds/correct.wav")
    wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")
    pygame.mixer.music.load("sounds/african_drum.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    print("Sound files not found - running silently")
    jump_sound = shout_sound = correct_sound = wrong_sound = None

if jump_sound: jump_sound.set_volume(0.6)
if shout_sound: shout_sound.set_volume(0.8)
if correct_sound: correct_sound.set_volume(0.7)
if wrong_sound: wrong_sound.set_volume(0.7)

def draw_traditional_bg(surface):
    surface.fill((245, 222, 179))
    for i in range(0, SCREEN_WIDTH, 50):
        pygame.draw.circle(surface, (150, 75, 0), (i, 100), 20)
        pygame.draw.circle(surface, (139, 69, 19), (i + 25, 150), 15)
    for j in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(surface, (101, 67, 33), (0, j), (SCREEN_WIDTH, j), 3)
        pygame.draw.line(surface, (101, 67, 33), (j, 0), (j, SCREEN_HEIGHT), 3)
    for k in range(0, SCREEN_WIDTH, 100):
        points = [(k, 200), (k+20, 180), (k+40, 220), (k+60, 180), (k+80, 220)]
        pygame.draw.lines(surface, (80, 50, 20), False, points, 5)
    pygame.draw.polygon(surface, (34, 139, 34), [(100, 300), (150, 280), (200, 320), (150, 340)])

class Player(pygame.sprite.Sprite):
    def __init__(self):  # Fixed method name from init to __init__
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        pygame.draw.circle(self.image, (255, 220, 177), (20, 10), 15)
        pygame.draw.rect(self.image, BLACK, (15, 25, 10, 20))
        pygame.draw.line(self.image, BLACK, (15, 30), (5, 45), 3)
        pygame.draw.line(self.image, BLACK, (25, 30), (35, 45), 3)
        pygame.draw.line(self.image, BLACK, (10, 50), (5, 65), 4)
        pygame.draw.line(self.image, BLACK, (30, 50), (35, 65), 4)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100)
        self.jumping = False
        self.jump_count = 10
        self.should_jump = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0: self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - 50: self.rect.x += 5
        
        if self.should_jump:
            self.jumping = True
            self.should_jump = False
            if jump_sound: jump_sound.play()
        
        if self.jumping:
            if self.jump_count >= -10:
                self.rect.y -= (self.jump_count * abs(self.jump_count)) * 0.5
                self.jump_count -= 1
            else:
                self.jumping = False
                self.jump_count = 10
                self.rect.y = SCREEN_HEIGHT - 100

    def jump(self):
        if not self.jumping: self.should_jump = True

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Fixed method name from init to __init__
        super().__init__()
        self.image = pygame.Surface((35, 55))
        self.image.fill(GREEN)
        pygame.draw.circle(self.image, (255, 220, 177), (17, 10), 12)
        pygame.draw.rect(self.image, BLACK, (12, 22, 11, 18))
        self.rect = self.image.get_rect(center=(x, y))

class Leader(pygame.sprite.Sprite):
    def __init__(self):  # Fixed method name from init to __init__
        super().__init__()
        self.image = pygame.Surface((45, 65))
        self.image.fill(RED)
        pygame.draw.circle(self.image, (255, 200, 150), (22, 12), 16)
        pygame.draw.rect(self.image, BLACK, (15, 28, 15, 22))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        self.anim_timer = 0
        self.anim_state = 0
        self.shout_timer = 0

    def update(self):
        self.anim_timer += 1
        self.shout_timer += 1
        if self.shout_timer > 180:
            if shout_sound: shout_sound.play()
            self.anim_state = 1
            self.shout_timer = 0
        if self.anim_timer > 30:
            self.anim_state = 0
            self.anim_timer = 0
        if self.anim_state == 1:
            self.rect.x += random.randint(-2, 2)

# Game setup
all_sprites = pygame.sprite.Group()
player = Player()
leader = Leader()
npcs = pygame.sprite.Group()

# Fixed the angle calculation - using math.radians and math.cos/sin
for i in range(8):
    angle = (i / 8) * 2 * math.pi  # Use math.pi instead of 3.14
    radius_x = 150
    radius_y = 100
    x = SCREEN_WIDTH // 2 + radius_x * math.cos(angle)
    y = SCREEN_HEIGHT // 2 + radius_y * math.sin(angle)
    npc = NPC(x, y)
    npcs.add(npc)
    all_sprites.add(npc)

all_sprites.add(player, leader)

animals = ["Cow", "Goat", "Chicken", "Dog", "Pig", "Elephant", "Zebra"]
edible = ["Cow", "Goat", "Chicken", "Zebra"]
current_animal = random.choice(animals)
player_score = 0
game_over = False
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

instructions = [
    "Arrow keys: Move | SPACE: Jump on edible animals!",
    "Edible: Cow, Goat, Chicken, Zebra",
    "Press R to restart | Sounds ON!"
]

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                if current_animal in edible:
                    if correct_sound: correct_sound.play()
                    player_score += 10
                else:
                    if wrong_sound: wrong_sound.play()
            if event.key == pygame.K_r and game_over:
                player_score = 0
                game_over = False
                player.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100)
                for npc in npcs: npc.kill()
                npcs.empty()
                # Fixed the restart code with correct angle calculation
                for i in range(8):
                    angle = (i / 8) * 2 * math.pi
                    radius_x = 150
                    radius_y = 100
                    x = SCREEN_WIDTH // 2 + radius_x * math.cos(angle)
                    y = SCREEN_HEIGHT // 2 + radius_y * math.sin(angle)
                    npc = NPC(x, y)
                    npcs.add(npc)
                    all_sprites.add(npc)

    if not game_over:
        all_sprites.update()
        if random.randint(1, 200) == 1 and len(npcs) > 1:
            eliminated_npc = random.choice(list(npcs))
            eliminated_npc.kill()
        if len(npcs) == 0:
            game_over = True

    draw_traditional_bg(screen)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))

    animal_text = small_font.render(f"Animal: {current_animal}", True, BLACK)
    screen.blit(animal_text, (10, 10))
    score_text = font.render(f"Score: {player_score}", True, BLACK)
    screen.blit(score_text, (10, 50))
    
    if game_over:
        win_text = font.render("YOU WIN! Final Score: " + str(player_score), True, RED)
        screen.blit(win_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

    for i, instr in enumerate(instructions):
        instr_text = small_font.render(instr, True, WHITE)
        screen.blit(instr_text, (SCREEN_WIDTH - 280, 10 + i * 25))

    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
sys.exit()