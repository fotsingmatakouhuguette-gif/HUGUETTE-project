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

def draw_text(text, font, color, x, y, center=True):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y)) if center else txt.get_rect(topleft=(x, y))
    screen.blit(txt, rect)

def draw_box(x, y, width, height, color, border_color=WHITE, border_width=2):
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), border_width)

def draw_button(text, font, text_color, box_color, x, y, width, height, selected=False):
    if selected:
        draw_box(x, y, width, height, SELECTED_BOX_COLOR, YELLOW, 3)
    else:
        draw_box(x, y, width, height, box_color, WHITE, 2)
    draw_text(text, font, text_color, x + width//2, y + height//2)

def how_to_play_screen():
    while True:
        screen.fill(BG_COLOR)
        draw_text("HOW TO PLAY", FONT_BIG, WHITE, WIDTH//2, 60)
        
        draw_box(150, 120, 600, 300, BOX_COLOR, BLUE, 3)
        
        lines = [
            "A category and a word are displayed.",
            "Decide if the word belongs to the category.",
            "Press Y for YES, N for NO.",
            "You have 3 lives.",
            "Timer reduces as levels increase.",
            "High score is saved automatically.",
            "Press ESC to return to menu."
        ]
        y = 150
        for line in lines:
            draw_text(line, FONT_MED, WHITE, WIDTH//2, y)
            y += 35

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        pygame.display.update()
        clock.tick(60)

def pause_menu():
    options = ["Resume", "Restart", "Main Menu"]
    
    while True:
        #screen.blit(image,(0,0))
        screen.fill(BG_COLOR)
        draw_text("PAUSED", FONT_BIG, YELLOW, WIDTH//2, 80)
       
        # Create button rectangles
        button_rects = []
        y = 180
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(WIDTH//2 - 100, y, 200, 45)
            button_rects.append(button_rect)
            
            # Check if mouse is hovering over button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            draw_button(opt, FONT_MED, YELLOW if is_hovering else WHITE, 
                       BOX_COLOR, button_rect.x, button_rect.y, button_rect.width, button_rect.height, False)
            y += 60

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(e.pos):
                        if i == 0:
                            return "resume"
                        elif i == 1:
                            return "restart"
                        elif i == 2:
                            return "menu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "resume"

        pygame.display.update()
        clock.tick(60)

def game_over_menu(score, high_score):
    while True:
        screen.fill(BG_COLOR)
        draw_text("GAME OVER", FONT_BIG, RED, WIDTH//2, 80)
        draw_text(f"Your score: {score}", FONT_MED, WHITE, WIDTH//2, 150)
        draw_text(f"High score: {high_score}", FONT_MED, WHITE, WIDTH//2, 200)
        
        options = ["Play Again", "Main Menu"]
        button_rects = []
        y = 280
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(WIDTH//2 - 100, y, 200, 45)
            button_rects.append(button_rect)
            
            # Check if mouse is hovering over button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            draw_button(opt, FONT_MED, YELLOW if is_hovering else WHITE, 
                       BOX_COLOR, button_rect.x, button_rect.y, button_rect.width, button_rect.height, False)
            y += 60

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(e.pos):
                        if i == 0:
                            return play_game()
                        elif i == 1:
                            return main_menu()

        pygame.display.update()
        clock.tick(60)

def decide_next_answer(last_correct_answer, consecutive_correct_same):
    if consecutive_correct_same >= 2:
        return not last_correct_answer
    else:
        return random.choice([True, False])

def play_game():
    global high_score
    score = 0
    lives = 3
    level = 1
    correct = 0
    last_answer = None
    consecutive_same = 0
    last_correct_answer = None
    consecutive_correct_same = 0

    duration = 4
    start = time.time()

    cat, words, category_truth = random.choice(categories)
    word = random.choice(words)
    
    # Decide answer with variety control
    force_yes = decide_next_answer(last_correct_answer, consecutive_correct_same)
    
    if force_yes:
        # Find a word that belongs to the category
        truth = True
        if not category_truth:
            # For NOT categories, we need to flip the logic
            truth = False
            # Find a word that doesn't belong to NOT category
            all_categories = [c for c in categories if c[0] != cat]
            if all_categories:
                other_cat, other_words, _ = random.choice(all_categories)
                word = random.choice(other_words)
    else:
        # Find a word that doesn't belong to the category
        truth = False
        if category_truth:
            # For regular categories, find a word from another category
            all_categories = [c for c in categories if c[0] != cat]
            if all_categories:
                other_cat, other_words, _ = random.choice(all_categories)
                word = random.choice(other_words)
        else:
            # For NOT categories, find a word that belongs to the category
            truth = True

    while True:
        screen.fill(BG_COLOR)
        

        elapsed = time.time() - start
        remaining = max(0, duration - elapsed)

        # Calculate dynamic box sizes
        category_text = f"Category: {cat}"
        category_surface = FONT_MED.render(category_text, True, YELLOW)
        category_width = category_surface.get_width() + 40  # Add padding
        category_height = category_surface.get_height() + 20
        
        word_surface = FONT_BIG.render(word, True, WHITE)
        word_width = word_surface.get_width() + 40  # Add padding
        word_height = word_surface.get_height() + 20
        
        # Draw category box with dynamic size
        draw_box(WIDTH//2 - category_width//2, 30, category_width, category_height, BOX_COLOR, YELLOW, 2)
        draw_text(category_text, FONT_MED, YELLOW, WIDTH//2, 60)
        
        # Draw word box with dynamic size
        draw_box(WIDTH//2 - word_width//2, 120, word_width, word_height, BOX_COLOR, GREEN, 3)
        draw_text(word, FONT_BIG, WHITE, WIDTH//2, 160)

        pygame.draw.rect(screen, (60,60,60), (250, 220, 400, 12))
        pygame.draw.rect(screen, RED, (250, 220, int((remaining/duration)*400), 12))

        draw_text(f"Score: {score}", FONT_SMALL, WHITE, 20, 20, False)
        draw_text(f"Lives: {lives}", FONT_SMALL, WHITE, 20, 45, False)
        draw_text(f"Level: {level}", FONT_SMALL, WHITE, 20, 70, False)
        draw_text(f"High Score: {high_score}", FONT_SMALL, WHITE, WIDTH-200, 20, False)
        
        # Pause button in top-right corner
        pause_button_rect = pygame.Rect(WIDTH - 120, 50, 100, 40)
        draw_button("PAUSE", FONT_SMALL, WHITE, BOX_COLOR, pause_button_rect.x, pause_button_rect.y, pause_button_rect.width, pause_button_rect.height)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(e.pos):
                    result = pause_menu()
                    if result == "resume":
                        start = time.time() - elapsed
                    elif result == "restart":
                        return play_game()
                    elif result == "menu":
                        return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    result = pause_menu()
                    if result == "resume":
                        start = time.time() - elapsed
                    elif result == "restart":
                        return play_game()
                    elif result == "menu":
                        return
                if e.key in (pygame.K_y, pygame.K_n):
                    answer = (e.key == pygame.K_y)
                    
                    # Check if same answer as last time
                    if answer == last_answer:
                        consecutive_same += 1
                        # Only lose life if same answer 2+ times in a row
                        if consecutive_same >= 2:
                            if answer != truth:
                                lives -= 1
                    else:
                        consecutive_same = 0
                        if answer != truth:
                            lives -= 1
                    
                    last_answer = answer
                    
                    if answer == truth:
                        score += 1
                        correct += 1
                        # Track correct answers for variety
                        if truth == last_correct_answer:
                            consecutive_correct_same += 1
                        else:
                            consecutive_correct_same = 1
                        last_correct_answer = truth

                    cat, words, category_truth = random.choice(categories)
                    word = random.choice(words)
                    
                    # Decide answer with variety control
                    force_yes = decide_next_answer(last_correct_answer, consecutive_correct_same)
                    
                    if force_yes:
                        # Find a word that belongs to the category
                        truth = True
                        if not category_truth:
                            # For NOT categories, we need to flip the logic
                            truth = False
                            # Find a word that doesn't belong to NOT category
                            all_categories = [c for c in categories if c[0] != cat]
                            if all_categories:
                                other_cat, other_words, _ = random.choice(all_categories)
                                word = random.choice(other_words)
                    else:
                        # Find a word that doesn't belong to the category
                        truth = False
                        if category_truth:
                            # For regular categories, find a word from another category
                            all_categories = [c for c in categories if c[0] != cat]
                            if all_categories:
                                other_cat, other_words, _ = random.choice(all_categories)
                                word = random.choice(other_words)
                        else:
                            # For NOT categories, find a word that belongs to the category
                            truth = True
                    start = time.time()

        if remaining <= 0:
            lives -= 1
            cat, words, category_truth = random.choice(categories)
            word = random.choice(words)
            
            # Decide answer with variety control
            force_yes = decide_next_answer(last_correct_answer, consecutive_correct_same)
            
            if force_yes:
                # Find a word that belongs to the category
                truth = True
                if not category_truth:
                    # For NOT categories, we need to flip the logic
                    truth = False
                    # Find a word that doesn't belong to NOT category
                    all_categories = [c for c in categories if c[0] != cat]
                    if all_categories:
                        other_cat, other_words, _ = random.choice(all_categories)
                        word = random.choice(other_words)
            else:
                # Find a word that doesn't belong to the category
                truth = False
                if category_truth:
                    # For regular categories, find a word from another category
                    all_categories = [c for c in categories if c[0] != cat]
                    if all_categories:
                        other_cat, other_words, _ = random.choice(all_categories)
                        word = random.choice(other_words)
                else:
                    # For NOT categories, find a word that belongs to the category
                    truth = True
            start = time.time()

        if correct >= 3:
            correct = 0
            level += 1
            duration = max(1.5, duration - 0.5)

        if lives <= 0:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_menu(score, high_score)
            return

        pygame.display.update()
        clock.tick(60)

def main_menu():
    options = ["Start", "How to Play", "Quit"]
    
    while True:
        screen.fill(BG_COLOR)
        
        draw_box(WIDTH//2 - 200, 40, 400, 80, BOX_COLOR, PURPLE, 3)
        draw_text("NYAMA NYAMA", FONT_BIG, WHITE, WIDTH//2, 80)
        
        # Create button rectangles
        button_rects = []
        y = 180
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(WIDTH//2 - 100, y, 200, 45)
            button_rects.append(button_rect)
            
            # Check if mouse is hovering over button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            draw_button(opt, FONT_MED, YELLOW if is_hovering else WHITE, 
                       BOX_COLOR, button_rect.x, button_rect.y, button_rect.width, button_rect.height, False)
            y += 60

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(e.pos):
                        if i == 0:
                            play_game()
                        elif i == 1:
                            how_to_play_screen()
                        elif i == 2:
                            sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    pass
                if e.key == pygame.K_DOWN:
                    pass
                if e.key == pygame.K_RETURN:
                    pass

        pygame.display.update()
        clock.tick(60)

main_menu()