import pygame
import random
import math

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
GAP_SIZE = 32
#-----------------GAME STATES-----------------
MENU="menu"
PLAYING="playing"
PAUSED="pause"
HOW_TO_PLAY="how to play"
ABOUT="about"

game_state= MENU

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

# ---------------- MAIN GAME ----------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2 Player Knock-Out")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    enemies = []
    for _ in range(TOTAL_ENEMIES):
        x = random.randint(SQUARE_X + BALL_RADIUS, SQUARE_X + SQUARE_SIZE - BALL_RADIUS)
        y = random.randint(SQUARE_Y + BALL_RADIUS, SQUARE_Y + SQUARE_SIZE - BALL_RADIUS)
        enemies.append(Ball(x, y, (255, 0, 0)))

    player_ball = Ball(WIDTH // 2, HEIGHT - 40, (0, 0, 255))

    aiming = False
    start_pos = (0, 0)
    current_player = 0
    scores = [0, 0]
    turn_active = False
    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not aiming and not turn_active and not game_over:
                aiming = True
                start_pos = (player_ball.x, player_ball.y)

            if event.type == pygame.MOUSEBUTTONUP and aiming:
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
        if turn_active:
            player_ball.move()
            for e in enemies:
                e.move()
                ball_collision(player_ball, e)

            # Enemy collisions
            for i in range(len(enemies)):
                for j in range(i + 1, len(enemies)):
                    ball_collision(enemies[i], enemies[j])

            # Wall + gap logic
            for e in enemies:
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

            # Check escaped balls
            escaped = 0
            for e in enemies[:]:
                if (e.x < SQUARE_X - BALL_RADIUS or
                    e.x > SQUARE_X + SQUARE_SIZE + BALL_RADIUS or
                    e.y < SQUARE_Y - BALL_RADIUS or
                    e.y > SQUARE_Y + SQUARE_SIZE + BALL_RADIUS):
                    enemies.remove(e)
                    escaped += 1

            scores[current_player] += escaped

            # End of turn when player ball stops
            if player_ball.vx == 0 and player_ball.vy == 0:
                player_ball.x = WIDTH // 2
                player_ball.y = HEIGHT - 40
                turn_active = False

                # Switch player ONLY if no ball escaped
                if escaped == 0:
                    current_player = 1 - current_player

        if len(enemies) == 0:
            game_over = True

        # ---------------- DRAW ----------------
        screen.fill((235, 235, 235))
        pygame.draw.rect(screen, (0, 0, 0),
                         (SQUARE_X, SQUARE_Y, SQUARE_SIZE, SQUARE_SIZE), 2)
        

         # Draw gaps
        pygame.draw.rect(screen, (240, 240, 240),
            (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (240, 240, 240),
            (SQUARE_X + SQUARE_SIZE//2 - GAP_SIZE//2, SQUARE_Y + SQUARE_SIZE - 2, GAP_SIZE, 4))
        pygame.draw.rect(screen, (240, 240, 240),
            (SQUARE_X - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))
        pygame.draw.rect(screen, (240, 240, 240),
            (SQUARE_X + SQUARE_SIZE - 2, SQUARE_Y + SQUARE_SIZE//2 - GAP_SIZE//2, 4, GAP_SIZE))

        for e in enemies:
            e.draw(screen)
        player_ball.draw(screen)

        if aiming:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (0, 0, 255), start_pos, (mx, my), 2)

        screen.blit(font.render(f"Player 1: {scores[0]}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Player 2: {scores[1]}", True, (0, 0, 0)), (10, 40))
        screen.blit(font.render(f"Turn: Player {current_player + 1}", True, (0, 0, 150)), (10, 70))

        if game_over:
            winner = "DRAW"
            if scores[0] > scores[1]:
                winner = "PLAYER 1 WINS"
            elif scores[1] > scores[0]:
                winner = "PLAYER 2 WINS"

            screen.blit(font.render(winner, True, (0, 150, 0)),
                        (WIDTH//2 - 90, HEIGHT//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
