import pygame
import random
import math
from sys import exit
import os
#--------------GAMES----------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.mixer.init()
# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60

SQUARE_SIZE = 220
SQUARE_X = (WIDTH - SQUARE_SIZE) // 2
SQUARE_Y = (HEIGHT - SQUARE_SIZE) // 2

BALL_RADIUS = 10
PLAYER_POWER = 7
FRICTION = 0.99
STOP_THRESHOLD = 0.1

TOTAL_ENEMIES = 10
GAP_SIZE = 40

# ---------- SCREEN ----------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Knock-Out")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# ---------------- GAME STATES ----------------
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
ABOUT="about"
HOW_TO_PLAY="how to play"

game_state = MENU

# ---------------- BUTTONS ----------------
start_button = pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/start.png").convert_alpha(),(200, 80)
)
start_button_rect = start_button.get_rect(center=(400,220))

pause_button = pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/pause.png").convert_alpha(),(80, 50)
)
pause_button_rect= pause_button.get_rect(topleft=(718,10))

resume_button = pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/resume.png").convert_alpha(),(200, 50)
)
resume_button_rect = resume_button.get_rect(center=(400,250))

restart_button = pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/restart.png").convert_alpha(),(200, 50)
)
restart_button_rect = restart_button.get_rect(center=(400,320))

about_button= pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/about.png").convert_alpha(),(200,80)
)
about_button_rect= about_button.get_rect(center=(400,430))

how_to_play_button=pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/how to play.png").convert_alpha(),(210,90)
)
how_to_play_button_rect= how_to_play_button.get_rect(center=(400,320))

menu_button=pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/back.png").convert_alpha(),(108,50)
)
menu_button_rect= menu_button.get_rect(topleft=(690,10))
title= pygame.transform.scale(
    pygame.image.load("marbble assets/buttons/Marble.png").convert_alpha(),(400,100)
)
title_rect= title.get_rect(center=(400,100))

#----------------BACKGROUNDS------------------
menu_back= pygame.transform.scale(pygame.image.load("marbble assets/backs/menu_back.png"),(WIDTH,HEIGHT))
#about_back= pygame.transform.scale(pygame.image.load("marbble assets/backs/menu_back.png"),(WIDTH,HEIGHT))
how_to_play_back= pygame.transform.scale(pygame.image.load("marbble assets/backs/how to play back.png"),(WIDTH,HEIGHT))
play_back=pygame.transform.scale(pygame.image.load("marbble assets/backs/playground.png"),(WIDTH,HEIGHT))

# ---------------- BALL CLASS ----------------
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= FRICTION
        self.vy *= FRICTION
        if abs(self.vx) < STOP_THRESHOLD:
            self.vx = 0
        if abs(self.vy) < STOP_THRESHOLD:
            self.vy = 0

    def draw(self, screen):
        # Draw outline
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), BALL_RADIUS + 2)
        # Draw the ball
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

# ---------------- COLLISION ----------------
def ball_collision(b1, b2):
    dx = b1.x - b2.x
    dy = b1.y - b2.y
    dist = math.hypot(dx, dy)
    if dist == 0 or dist > BALL_RADIUS * 2:
        return
    nx = dx / dist
    ny = dy / dist
    p = (b1.vx - b2.vx) * nx + (b1.vy - b2.vy) * ny
    b1.vx -= p * nx
    b1.vy -= p * ny
    b2.vx += p * nx
    b2.vy += p * ny

# ---------------- RED BALLS COLLISION ----------------
def red_ball_collision(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]

            dx = b2.x - b1.x
            dy = b2.y - b1.y
            dist = math.hypot(dx, dy)
            if dist == 0 or dist > BALL_RADIUS * 2:
                continue

            nx = dx / dist
            ny = dy / dist

            overlap = BALL_RADIUS * 2 - dist
            b1.x -= nx * overlap / 2
            b1.y -= ny * overlap / 2
            b2.x += nx * overlap / 2
            b2.y += ny * overlap / 2

            b1.vx, b2.vx = b2.vx, b1.vx
            b1.vy, b2.vy = b2.vy, b1.vy

# ---------------- RESET GAME ----------------
def reset_game():
    global enemies, player_ball, scores, current_player
    global turn_active, aiming, game_state

    enemies = []
    for _ in range(TOTAL_ENEMIES):
        x = random.randint(SQUARE_X + BALL_RADIUS, SQUARE_X + SQUARE_SIZE - BALL_RADIUS)
        y = random.randint(SQUARE_Y + BALL_RADIUS, SQUARE_Y + SQUARE_SIZE - BALL_RADIUS)
        enemies.append(Ball(x, y, (255, 0, 0)))

    player_ball.x = WIDTH // 2
    player_ball.y = HEIGHT - 40
    player_ball.vx = player_ball.vy = 0

    scores = [0, 0]
    current_player = 0
    turn_active = False
    aiming = False
    game_state = PLAYING

# ---------------- MAIN ----------------
button_sound = pygame.mixer.Sound("marbble assets/songs/button_click.wav")
button_sound.set_volume(0.5)
pygame.mixer.music.load("marbble assets/songs/Savanna Sprint.mp3")
pygame.mixer.music.play(-1)
wall_sound = pygame.mixer.Sound("marbble assets/songs/wall_hit.wav")
wall_sound.set_volume(0.5)


player_ball = Ball(WIDTH // 2, HEIGHT - 40, (0, 0, 255))
enemies = []
scores = [0, 0]
current_player = 0
turn_active = False
aiming = False
start_pos = (0, 0)

running = True
while running:
    clock.tick(FPS)

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and game_state == PLAYING:
                game_state = PAUSED
            elif event.key == pygame.K_p and game_state == PAUSED:
                game_state = PLAYING
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_state == MENU:
                if start_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    button_sound.play()
                elif about_button_rect.collidepoint(mouse_pos):
                    game_state=ABOUT
                    button_sound.play()
                elif how_to_play_button_rect.collidepoint(mouse_pos):
                    game_state=HOW_TO_PLAY
                    button_sound.play()
            elif game_state == PLAYING:
                if pause_button_rect.collidepoint(mouse_pos):
                    game_state = PAUSED
                    button_sound.play()
                elif not aiming and not turn_active:
                    aiming = True
                    start_pos = (player_ball.x, player_ball.y)
            elif game_state == PAUSED:
                if resume_button_rect.collidepoint(mouse_pos):
                    game_state = PLAYING
                    button_sound.play()
                elif restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    button_sound.play()
                elif menu_button_rect.collidepoint(mouse_pos):
                     game_state = MENU
                     button_sound.play()
            elif game_state == GAME_OVER:
                if restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
                    button_sound.play()
                elif menu_button_rect.collidepoint(mouse_pos):
                     game_state = MENU
                     button_sound.play()
            elif menu_button_rect.collidepoint(mouse_pos):
                if game_state in (HOW_TO_PLAY,ABOUT,GAME_OVER,PAUSED):
                    game_state=MENU
                    button_sound.play()
        if event.type == pygame.MOUSEBUTTONUP and aiming and game_state == PLAYING:
            aiming = False
            mx, my = pygame.mouse.get_pos()
            dx = start_pos[0] - mx
            dy = start_pos[1] - my
            dist = math.hypot(dx, dy)
            if dist > 0:
                player_ball.vx = (dx / dist) * PLAYER_POWER
                player_ball.vy = (dy / dist) * PLAYER_POWER
                turn_active = True

    # ---------------- UPDATE ----------------
    if game_state == PLAYING and turn_active:
        player_ball.move()
        escaped = 0
        for e in enemies[:]:
            e.move()
            ball_collision(player_ball, e)
            # WALL COLLISION WITH GAPS
            #LEFT
            if e.x - BALL_RADIUS <= SQUARE_X:
                if not (SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.y <=
                        SQUARE_Y + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.x = SQUARE_X + BALL_RADIUS
                    e.vx *= -1
                    wall_sound.play()
            #RIGHT
            if e.x + BALL_RADIUS >= SQUARE_X + SQUARE_SIZE:
                if not (SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.y <=
                        SQUARE_Y + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.x = SQUARE_X + SQUARE_SIZE - BALL_RADIUS
                    e.vx *= -1
                    wall_sound.play()
            #TOP
            if e.y - BALL_RADIUS <= SQUARE_Y:
                if not (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.x <=
                        SQUARE_X + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.y = SQUARE_Y + BALL_RADIUS
                    e.vy *= -1
                    wall_sound.play()
            #BOTTOM
            if e.y + BALL_RADIUS >= SQUARE_Y + SQUARE_SIZE:
                if not (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.x <=
                        SQUARE_X + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.y = SQUARE_Y + SQUARE_SIZE - BALL_RADIUS
                    e.vy *= -1
                    wall_sound.play()
                    
            # ESCAPE THROUGH GAP
            if (e.x < SQUARE_X - BALL_RADIUS or
                e.x > SQUARE_X + SQUARE_SIZE + BALL_RADIUS or
                e.y < SQUARE_Y - BALL_RADIUS or
                e.y > SQUARE_Y + SQUARE_SIZE + BALL_RADIUS):
                enemies.remove(e)
                escaped += 1

        # RED BALL COLLISION
        red_ball_collision(enemies)

        scores[current_player] += escaped

        if player_ball.vx == 0 and player_ball.vy == 0:
            player_ball.x = WIDTH // 2
            player_ball.y = HEIGHT - 40
            turn_active = False
            if escaped == 0:
                current_player = 1 - current_player

    if len(enemies) == 0 and game_state == PLAYING:
        game_state = GAME_OVER

    # ---------------- DRAW ----------------
    screen.fill((235, 235, 235))
    if game_state == MENU:
        screen.blit(menu_back,(0,0))
        screen.blit(title,title_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(about_button, about_button_rect)
        screen.blit(how_to_play_button, how_to_play_button_rect)
    elif game_state==ABOUT:
        screen.blit(menu_back,(0,0))
        screen.blit(font.render("marbble game created  by nadriekoda",True,(0,0,0)),(200,230))
        screen.blit(menu_button,menu_button_rect)
    elif game_state==HOW_TO_PLAY:
        screen.blit(how_to_play_back,(0,0))
        screen.blit(font.render("drag the ball with the mouse,release and shoot ",True,(0,0,0)),(160,230))
        screen.blit(font.render("The balls must go out of the square",True,(0,0,0)),(230,260))
        screen.blit(menu_button,menu_button_rect)
    elif game_state == PLAYING:
        screen.blit(play_back,(0,0))
        pygame.draw.rect(screen, (0, 0, 0), (SQUARE_X, SQUARE_Y, SQUARE_SIZE, SQUARE_SIZE), 2)
        screen.blit(font.render(f"P1: {scores[0]}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"P2: {scores[1]}", True, (255, 255, 255)), (10, 40))
        screen.blit(font.render(f"Turn: Player {current_player + 1}", True, (255, 255, 255)), (10, 70))
        screen.blit(pause_button,pause_button_rect)
        # DRAW GAPS
        pygame.draw.rect(screen, (235,235,235),(SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (235,235,235),(SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y + SQUARE_SIZE - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (235,235,235),(SQUARE_X - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))
        pygame.draw.rect(screen, (235,235,235),(SQUARE_X + SQUARE_SIZE - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))
        for e in enemies:
            e.draw(screen)
        player_ball.draw(screen)
        if aiming:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (0, 0, 255), start_pos, (mx, my), 2)
    elif game_state == PAUSED:
        screen.blit(menu_back,(0,0))
        screen.blit(font.render("PAUSED", True, (0, 0, 0)), (350, 200))
        screen.blit(restart_button,restart_button_rect)
        screen.blit(resume_button, resume_button_rect)
        screen.blit(menu_button,menu_button_rect)
    elif game_state == GAME_OVER:
        screen.blit(menu_back,(0,0))
        winner = "DRAW"
        if scores[0] > scores[1]:
            screen.blit(font.render("PLAYER 1 WINS !",True,(0,0,0)),(350,230))
        elif scores[1] > scores[0]:
            screen.blit(font.render("PLAYER 2 WINS !",True,(0,0,0)),(350,230))
        elif scores[0] == scores[1]:
            screen.blit(font.render("DRAW !!",True,(0,0,0)),(350,230))
        screen.blit(font.render(winner, True, (0, 150, 0)),(WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_button,restart_button_rect)
        screen.blit(menu_button,menu_button_rect)

    pygame.display.flip()
