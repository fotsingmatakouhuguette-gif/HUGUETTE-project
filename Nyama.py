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

#-----------------GAME STATES------------------
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
ABOUT = "about"
HOW_TO_PLAY = "how_to_play"

game_state = MENU

# ---------------- FONTS ----------------
FONT_BIG = pygame.font.SysFont("arialblack", 46)
FONT_MED = pygame.font.SysFont("arial", 26)
FONT_SMALL = pygame.font.SysFont("arial", 20)

# ---------------- COLORS ----------------
BG_COLOR = (25, 25, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (200, 70, 70)
GREEN = (70, 200, 120)
BLUE = (70, 130, 200)

# ---------------- HIGH SCORE ----------------
HS_FILE = "highscore.txt"

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

# ---------------- CATEGORIES ----------------
categories = [
    ("EDIBLE FOOD", ["Fish","Snake","Pork","Chicken","Cat"], True),
    ("NOT EDIBLE", ["Dog","Turtle","Pufferfish","Scorpion"], False),
    ("FOOTBALL PLAYER", ["Cristiano Ronaldo","Lionel Messi","Neymar Junior","Karim Benzema","Marco Reus"], True),
    ("BASKETBALL PLAYER", ["Lebron James","Steph Curry","Anthony Edwards","Ja Morant","Klay Thompson"], True),
    ("CAR BRAND", ["Mercedes","Toyota","Tesla","Ford","Rolls Royce"], True),
    ("NOT CARS", ["Toshiba","Nanfan","Oreimo","Apple","Optimus"], False),
    ("BOYS NAME", ["Ivan","Stephane","Jorge","Kris","Justin","Karis"], True),
    ("GIRLS NAME", ["Blessing","Karen","Stella","Ange"], True)
]

# ---------------- HELPER FUNCTIONS ----------------
def draw_text(text, font, color, x, y, center=True):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y)) if center else txt.get_rect(topleft=(x, y))
    screen.blit(txt, rect)

def draw_button(text, x, y, width, height, color, hover_color, hover=False):
    button_color = hover_color if hover else color
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=8)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=8)
    draw_text(text, FONT_MED, WHITE, x + width//2, y + height//2)

# ---------------- GAME VARIABLES ----------------
score = 0
lives = 3
level = 1
correct = 0
duration = 6
start_time = 0
current_category = None
current_words = None
current_truth = None
current_word = None
selected_option = 0
menu_options = ["Start Game", "How to Play", "About", "Quit"]
about_page = 0
how_to_play_page = 0

# ---------------- RESET GAME ----------------
def reset_game():
    global score, lives, level, correct, duration
    global start_time, current_category, current_words, current_truth, current_word
    
    score = 0
    lives = 3
    level = 1
    correct = 0
    duration = 6
    
    # Initialize first question
    current_category, current_words, current_truth = random.choice(categories)
    current_word = random.choice(current_words)
    start_time = time.time()

# ---------------- STATE HANDLERS ----------------
def handle_menu():
    global game_state, selected_option
    
    screen.fill(BG_COLOR)
    draw_text("NYAMA NYAMA", FONT_BIG, YELLOW, WIDTH//2, 80)
    
    # Draw menu options
    y = 180
    for i, option in enumerate(menu_options):
        color = YELLOW if i == selected_option else WHITE
        draw_text(option, FONT_MED, color, WIDTH//2, y)
        y += 50
    
    # Draw high score
    draw_text(f"High Score: {high_score}", FONT_SMALL, GREEN, WIDTH//2, HEIGHT - 50)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game
                    reset_game()
                    game_state = PLAYING
                elif selected_option == 1:  # How to Play
                    game_state = HOW_TO_PLAY
                elif selected_option == 2:  # About
                    game_state = ABOUT
                elif selected_option == 3:  # Quit
                    pygame.quit()
                    sys.exit()

def handle_playing():
    global game_state, score, lives, level, correct, duration, high_score
    global start_time, current_category, current_words, current_truth, current_word
    
    screen.fill(BG_COLOR)
    
    # Calculate time remaining
    elapsed = time.time() - start_time
    remaining = max(0, duration - elapsed)
    
    # Draw category and word
    draw_text(f"Category: {current_category}", FONT_MED, YELLOW, WIDTH//2, 50)
    draw_text(current_word, FONT_BIG, WHITE, WIDTH//2, 130)
    
    # Draw timer bar
    pygame.draw.rect(screen, (60, 60, 60), (250, 200, 400, 12))
    pygame.draw.rect(screen, RED, (250, 200, int((remaining/duration)*400), 12))
    
    # Draw controls
    draw_text("Press Y for YES, N for NO", FONT_SMALL, GREEN, WIDTH//2, 230)
    
    # Draw stats
    draw_text(f"Score: {score}", FONT_SMALL, WHITE, 20, 20, False)
    draw_text(f"Lives: {lives}", FONT_SMALL, WHITE, 20, 45, False)
    draw_text(f"Level: {level}", FONT_SMALL, WHITE, 20, 70, False)
    draw_text(f"High Score: {high_score}", FONT_SMALL, WHITE, WIDTH-200, 20, False)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU
            
            if event.key in (pygame.K_y, pygame.K_n):
                answer = (event.key == pygame.K_y)
                if answer == current_truth:
                    score += 1
                    correct += 1
                else:
                    lives -= 1
                    score -= 1

                # Get new question
                current_category, current_words, current_truth = random.choice(categories)
                current_word = random.choice(current_words)
                start_time = time.time()
    
    # Check timer
    if remaining <= 0:
        lives -= 1
        current_category, current_words, current_truth = random.choice(categories)
        current_word = random.choice(current_words)
        start_time = time.time()
    
    # Level progression
    if correct >= 5:
        correct = 0
        level += 1
        duration = max(2, duration - 1)
    
    # Check game over
    if lives <= 0:
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        game_state = GAME_OVER

def handle_paused():
    global game_state
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    draw_text("GAME PAUSED", FONT_BIG, YELLOW, WIDTH//2, 150)
    
    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    
    # Resume button
    resume_hover = pygame.Rect(WIDTH//2 - 100, 220, 200, 50).collidepoint(mouse_pos)
    draw_button("RESUME", WIDTH//2 - 100, 220, 200, 50, BLUE, GREEN, resume_hover)
    
    # Restart button
    restart_hover = pygame.Rect(WIDTH//2 - 100, 290, 200, 50).collidepoint(mouse_pos)
    draw_button("RESTART", WIDTH//2 - 100, 290, 200, 50, RED, GREEN, restart_hover)
    
    # Menu button
    menu_hover = pygame.Rect(WIDTH//2 - 100, 360, 200, 50).collidepoint(mouse_pos)
    draw_button("MAIN MENU", WIDTH//2 - 100, 360, 200, 50, (100, 100, 100), GREEN, menu_hover)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                game_state = PLAYING
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check button clicks
            if pygame.Rect(WIDTH//2 - 100, 220, 200, 50).collidepoint(mouse_pos):
                game_state = PLAYING
            elif pygame.Rect(WIDTH//2 - 100, 290, 200, 50).collidepoint(mouse_pos):
                reset_game()
                game_state = PLAYING
            elif pygame.Rect(WIDTH//2 - 100, 360, 200, 50).collidepoint(mouse_pos):
                game_state = MENU

def handle_game_over():
    global game_state
    
    screen.fill(BG_COLOR)
    
    draw_text("GAME OVER", FONT_BIG, RED, WIDTH//2, 100)
    draw_text(f"Final Score: {score}", FONT_MED, WHITE, WIDTH//2, 180)
    draw_text(f"High Score: {high_score}", FONT_MED, YELLOW, WIDTH//2, 220)
    
    # Determine performance message
    if score == high_score and score > 0:
        draw_text("NEW HIGH SCORE!", FONT_MED, GREEN, WIDTH//2, 260)
    elif score > 20:
        draw_text("Excellent!", FONT_MED, GREEN, WIDTH//2, 260)
    elif score > 10:
        draw_text("Good Job!", FONT_MED, YELLOW, WIDTH//2, 260)
    elif score > 0:
        draw_text("Nice Try!", FONT_MED, WHITE, WIDTH//2, 260)
    
    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    
    # Restart button
    restart_hover = pygame.Rect(WIDTH//2 - 100, 320, 200, 50).collidepoint(mouse_pos)
    draw_button("PLAY AGAIN", WIDTH//2 - 100, 320, 200, 50, BLUE, GREEN, restart_hover)
    
    # Menu button
    menu_hover = pygame.Rect(WIDTH//2 - 100, 390, 200, 50).collidepoint(mouse_pos)
    draw_button("MAIN MENU", WIDTH//2 - 100, 390, 200, 50, (100, 100, 100), GREEN, menu_hover)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()
                game_state = PLAYING
            elif event.key == pygame.K_ESCAPE:
                game_state = MENU
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if pygame.Rect(WIDTH//2 - 100, 320, 200, 50).collidepoint(mouse_pos):
                reset_game()
                game_state = PLAYING
            elif pygame.Rect(WIDTH//2 - 100, 390, 200, 50).collidepoint(mouse_pos):
                game_state = MENU

def handle_about():
    global game_state
    
    screen.fill(BG_COLOR)
    draw_text("ABOUT THE GAME", FONT_BIG, WHITE, WIDTH//2, 60)
    
    lines = [
        "A category and a word are displayed.",
        "Decide if the word belongs to the category.",
        "Press Y for YES, N for NO.",
        "You have 3 lives.",
        "Timer reduces as levels increase.",
        "High score is saved automatically.",
        "",
        "Press ESC to return to menu."
    ]
    
    y = 150
    for line in lines:
        draw_text(line, FONT_MED, WHITE, WIDTH//2, y)
        y += 35
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU

def handle_how_to_play():
    global game_state
    
    screen.fill(BG_COLOR)
    draw_text("HOW TO PLAY", FONT_BIG, WHITE, WIDTH//2, 60)
    
    lines = [
        "1. A category and a word will appear on screen.",
        "2. Decide if the word belongs to the category.",
        "3. Press Y key for YES.",
        "4. Press N key for NO.",
        "",
        "GAME RULES:",
        "- You start with 3 lives.",
        "- Correct answer: +1 score",
        "- Wrong answer: -1 score, -1 life",
        "- Time out: -1 life",
        "- Every 5 correct answers = Level up",
        "- Timer gets faster each level",
        "",
        "Press ESC to return to menu."
    ]
    
    y = 120
    for line in lines:
        draw_text(line, FONT_SMALL, WHITE, WIDTH//2, y)
        y += 25
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU

# ---------------- MAIN GAME LOOP ----------------
def main():
    global game_state
    
    while True:
        # Handle different game states
        if game_state == MENU:
            handle_menu()
        elif game_state == PLAYING:
            handle_playing()
        elif game_state == PAUSED:
            handle_paused()
        elif game_state == GAME_OVER:
            handle_game_over()
        elif game_state == ABOUT:
            handle_about()
        elif game_state == HOW_TO_PLAY:
            handle_how_to_play()
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()