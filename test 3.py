import pygame
import random
import math
from sys import exit

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

# ---------------- GAME STATES ----------------
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
ABOUT="about"
HOW_TO_PLAY="how to play"

game_state = MENU

# ---------------- BUTTONS ----------------
start_button_rect = pygame.Rect(300, 200, 200, 50)
pause_button_rect = pygame.Rect(740, 10, 50, 30)
resume_button_rect = pygame.Rect(300, 250, 200, 50)
restart_button_rect = pygame.Rect(300, 320, 200, 50)
about_button_rect= pygame.Rect(300,320,200,50)
how_to_play_button_rect=pygame.Rect(270,260,260,50)
menu_button_rect=pygame.Rect(690,10,108,50)

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
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), BALL_RADIUS)

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
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Knock-Out")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

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
                elif about_button_rect.collidepoint(mouse_pos):
                    game_state=ABOUT
                elif how_to_play_button_rect.collidepoint(mouse_pos):
                    game_state=HOW_TO_PLAY

            elif game_state == PLAYING:
                if pause_button_rect.collidepoint(mouse_pos):
                    game_state = PAUSED
                elif not aiming and not turn_active:
                    aiming = True
                    start_pos = (player_ball.x, player_ball.y)

            elif game_state == PAUSED:
                if resume_button_rect.collidepoint(mouse_pos):
                    game_state = PLAYING
                elif restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
                elif menu_button_rect.collidepoint(mouse_pos):
                     game_state = MENU

            elif game_state == GAME_OVER:
                if restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
                elif menu_button_rect.collidepoint(mouse_pos):
                     game_state = MENU

            elif menu_button_rect.collidepoint(mouse_pos):
                if game_state in (HOW_TO_PLAY,ABOUT,GAME_OVER,PAUSED):
                    game_state=MENU

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

            # ---- WALLS WITH GAPS ----
            # LEFT
            if e.x - BALL_RADIUS <= SQUARE_X:
                if not (SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.y <=
                        SQUARE_Y + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.x = SQUARE_X + BALL_RADIUS
                    e.vx *= -1

            # RIGHT
            if e.x + BALL_RADIUS >= SQUARE_X + SQUARE_SIZE:
                if not (SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.y <=
                        SQUARE_Y + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.x = SQUARE_X + SQUARE_SIZE - BALL_RADIUS
                    e.vx *= -1

            # TOP
            if e.y - BALL_RADIUS <= SQUARE_Y:
                if not (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.x <=
                        SQUARE_X + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.y = SQUARE_Y + BALL_RADIUS
                    e.vy *= -1

            # BOTTOM
            if e.y + BALL_RADIUS >= SQUARE_Y + SQUARE_SIZE:
                if not (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2 <= e.x <=
                        SQUARE_X + SQUARE_SIZE//2 + GAP_SIZE//2):
                    e.y = SQUARE_Y + SQUARE_SIZE - BALL_RADIUS
                    e.vy *= -1

            # ---- ESCAPE THROUGH GAP ----
            if (e.x < SQUARE_X - BALL_RADIUS or
                e.x > SQUARE_X + SQUARE_SIZE + BALL_RADIUS or
                e.y < SQUARE_Y - BALL_RADIUS or
                e.y > SQUARE_Y + SQUARE_SIZE + BALL_RADIUS):
                enemies.remove(e)
                escaped += 1

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
        pygame.draw.rect(screen, (0, 150, 0), start_button_rect)
        pygame.draw.rect(screen,(0,150,0),about_button_rect)
        pygame.draw.rect(screen,(0,150,0),how_to_play_button_rect)
        screen.blit(font.render("START", True, (255, 255, 255)), (360, 215))
        screen.blit(font.render("ABOUT",True,(255,255,255)),(360,330))
        screen.blit(font.render("HOW TO PLAY",True,(255,255,255)),(320,275))
       

    elif game_state==ABOUT:
        screen.blit(font.render("marbble game created  by nadriekoda",True,(0,0,0)),(200,230))
        pygame.draw.rect(screen, (0, 150, 0), menu_button_rect)
        screen.blit(font.render("MENU",True,(255,255,255)),(710,25))

    elif game_state==HOW_TO_PLAY:
         screen.blit(font.render("drag the ball with the mouse and shoot",True,(0,0,0)),(200,230))
         pygame.draw.rect(screen, (0, 150, 0), menu_button_rect)
         screen.blit(font.render("MENU",True,(255,255,255)),(710,25))

    elif game_state == PLAYING:
        pygame.draw.rect(screen, (0, 0, 0),
            (SQUARE_X, SQUARE_Y, SQUARE_SIZE, SQUARE_SIZE), 2)
        screen.blit(font.render(f"P1: {scores[0]}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"P2: {scores[1]}", True, (0, 0, 0)), (10, 40))
        screen.blit(font.render(f"Turn: Player {current_player + 1}", True, (0, 0, 150)), (10, 70))


        # ---- DRAW GAPS ----
        pygame.draw.rect(screen, (235,235,235),
            (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (235,235,235),
            (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y + SQUARE_SIZE - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (235,235,235),
            (SQUARE_X - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))
        pygame.draw.rect(screen, (235,235,235),
            (SQUARE_X + SQUARE_SIZE - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))

        for e in enemies:
            e.draw(screen)
        player_ball.draw(screen)

        if aiming:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (0, 0, 255), start_pos, (mx, my), 2)

        pygame.draw.rect(screen, (200, 0, 0), pause_button_rect)
        screen.blit(font.render("||", True, (255, 255, 255)), (757, 12))

    elif game_state == PAUSED:
        screen.blit(font.render("PAUSED", True, (0, 0, 0)), (350, 200))
        pygame.draw.rect(screen, (0, 150, 0), resume_button_rect)
        pygame.draw.rect(screen, (150, 0, 0), restart_button_rect)
        pygame.draw.rect(screen, (0, 150, 0), menu_button_rect)
        screen.blit(font.render("RESUME", True, (255, 255, 255)), (350, 265))
        screen.blit(font.render("RESTART", True, (255, 255, 255)), (345, 335))
        screen.blit(font.render("MENU",True,(255,255,255)),(710,25))

    elif game_state == GAME_OVER:
        winner = "DRAW"
        if scores[0] > scores[1]:
            winner = "PLAYER 1 WINS"
        elif scores[1] > scores[0]:
            winner = "PLAYER 2 WINS"
   
        screen.blit(font.render(winner, True, (0, 150, 0)),
                    (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.draw.rect(screen, (150, 0, 0), restart_button_rect)
        pygame.draw.rect(screen, (0, 150, 0), menu_button_rect)
        screen.blit(font.render("RESTART", True, (255, 255, 255)), (345, 335))
        screen.blit(font.render("MENU",True,(255,255,255)),(710,25))


    pygame.display.flip()
