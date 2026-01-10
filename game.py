import pygame
import json
import random
import os
import textwrap  # <-- for wrapping long questions

# -------------------- LOAD RIDDLES --------------------
def load_riddles():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "riddles.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["riddles"]

# -------------------- MAIN GAME --------------------
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Cameroon Riddles Adventure")
    clock = pygame.time.Clock()

    riddles = load_riddles()
    asked_riddles = []

    player = pygame.Rect(50, 550, 40, 40)
    vel_y = 0
    ground = pygame.Rect(0, 600, 900, 50)

    obstacles = [
        pygame.Rect(300, 560, 50, 40),
        pygame.Rect(500, 560, 50, 40),
        pygame.Rect(700, 560, 50, 40),
    ]

    # ------------------ COLLISION FLAGS ------------------
    collision_flags = {id(obs): False for obs in obstacles}  # Track if player is already colliding

    # Fonts
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 48, bold=True)

    # Riddle state
    riddle_active = False
    current_riddle = None
    feedback_active = False
    feedback_text = ""
    feedback_color = (0, 255, 0)
    riddle_timer = 30
    remaining_time = riddle_timer
    riddle_start = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000  # seconds elapsed

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                if riddle_active and current_riddle:
                    key_map = {
                        pygame.K_1: 1, pygame.K_KP1: 1,
                        pygame.K_2: 2, pygame.K_KP2: 2,
                        pygame.K_3: 3, pygame.K_KP3: 3,
                        pygame.K_4: 4, pygame.K_KP4: 4,
                    }
                    if e.key in key_map:
                        choice = key_map[e.key]
                        if choice == current_riddle["answer"]:
                            feedback_text = "Correct!"
                            feedback_color = (0, 255, 0)
                        else:
                            feedback_text = "Wrong!"  # <-- no correct answer displayed
                            feedback_color = (255, 0, 0)

                        riddle_active = False
                        feedback_active = True
                        feedback_start = pygame.time.get_ticks()
                        current_riddle = None

        # ---- UPDATE ----
        keys = pygame.key.get_pressed()
        if not riddle_active and not feedback_active:
            if keys[pygame.K_LEFT]:
                player.x -= 6
            if keys[pygame.K_RIGHT]:
                player.x += 6

            vel_y += 1
            player.y += vel_y
            if player.colliderect(ground):
                player.bottom = ground.top
                vel_y = 0

            # -------- COLLISION CHECK --------
            for obs in obstacles:
                obs_id = id(obs)
                if player.colliderect(obs):
                    if not collision_flags[obs_id] and not riddle_active and not feedback_active:
                        available = [r for r in riddles if r not in asked_riddles]
                        if available:
                            current_riddle = random.choice(available)
                            asked_riddles.append(current_riddle)
                            riddle_active = True
                            riddle_start = pygame.time.get_ticks()
                            remaining_time = riddle_timer
                        collision_flags[obs_id] = True
                else:
                    collision_flags[obs_id] = False

        # Update riddle timer
        if riddle_active:
            elapsed = (pygame.time.get_ticks() - riddle_start) / 1000
            remaining_time = max(0, riddle_timer - int(elapsed))
            if remaining_time == 0:
                feedback_text = "Time's up!"
                feedback_color = (255, 0, 0)
                riddle_active = False
                feedback_active = True
                feedback_start = pygame.time.get_ticks()
                current_riddle = None

        # Feedback display duration
        if feedback_active:
            if pygame.time.get_ticks() - feedback_start > 1500:
                feedback_active = False

        # ---- DRAW ----
        screen.fill((50, 50, 100))
        pygame.draw.rect(screen, (150, 75, 0), ground)
        pygame.draw.rect(screen, (255, 100, 100), player)

        for obs in obstacles:
            pygame.draw.rect(screen, (0, 255, 0), obs)

        # Only draw riddle box if there is a current riddle
        if riddle_active and current_riddle:
            box_w, box_h = 700, 300
            box_x, box_y = (screen.get_width() - box_w) // 2, 100

            # Space for background
            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(screen, (255, 215, 0), (box_x, box_y, box_w, box_h), 4)

            # Wrap long question lines
            wrapped_lines = textwrap.wrap(current_riddle["question"], width=60)
            y = box_y + 20
            for line in wrapped_lines:
                q = font.render(line, True, (255, 255, 255))
                screen.blit(q, (box_x + 20, y))
                y += 25  # line spacing

            # Choices
            y = box_y + 100
            for k, v in current_riddle["choices"].items():
                txt = font.render(f"{k}) {v}", True, (200, 200, 200))
                screen.blit(txt, (box_x + 40, y))
                y += 35

            # Timer at bottom-right corner of riddle box
            timer_text = big_font.render(f"Time: {remaining_time}", True, (255, 0, 0))
            timer_x = box_x + box_w - timer_text.get_width() - 20
            timer_y = box_y + box_h - timer_text.get_height() - 10
            screen.blit(timer_text, (timer_x, timer_y))

        # Feedback box
        if feedback_active:
            box_w, box_h = 700, 300
            box_x, box_y = (screen.get_width() - box_w) // 2, 100
            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(screen, (255, 215, 0), (box_x, box_y, box_w, box_h), 4)
            feedback_render = big_font.render(feedback_text, True, feedback_color)
            fb_rect = feedback_render.get_rect(center=(box_x + box_w // 2, box_y + box_h // 2))
            screen.blit(feedback_render, fb_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_game()
