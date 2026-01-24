import pygame
import os
import subprocess
import sys

pygame.init()

# ---------- SCREEN SETUP ----------
WIDTH, HEIGHT = 800, 600  # Increased size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Launcher - Corrected Paths")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
HOVER_GREEN = (100, 255, 100)
HOVER_RED = (255, 100, 100)
YELLOW = (255, 200, 0)
PURPLE = (180, 100, 255)
HOVER_PURPLE = (220, 150, 255)

# ---------- GAME STATES ----------
MENU = "menu"
ABOUT = "about"
current_state = MENU

#-------------------------ASSETS---------------------------
# Load menu background
try:
    image = pygame.transform.scale(pygame.image.load("Launcher assets/menu_back.jpeg"), (WIDTH, HEIGHT))
except:
    # Fallback if image not found
    image = pygame.Surface((WIDTH, HEIGHT))
    image.fill((25, 25, 50))

# Load about us background if exists
try:
    screen.fill((0,0,0))
    about_image = pygame.transform.scale(pygame.image.load("Launcher assets/about us.png"), (WIDTH, HEIGHT))
except:
    # Fallback about image
    about_image = pygame.Surface((WIDTH, HEIGHT))
    about_image.fill((40, 40, 60))
    # Add text to fallback image
    title_font = pygame.font.Font(None, 60)
    title = title_font.render("ABOUT US", True, YELLOW)
    text_font = pygame.font.Font(None, 36)
    line1 = text_font.render("AFRI PLAY Game Launcher", True, WHITE)
    line2 = text_font.render("Version 3.0", True, WHITE)
    line3 = text_font.render("Created by Your Name", True, WHITE)
    about_image.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    about_image.blit(line1, (WIDTH//2 - line1.get_width()//2, 150))
    about_image.blit(line2, (WIDTH//2 - line2.get_width()//2, 200))
    about_image.blit(line3, (WIDTH//2 - line3.get_width()//2, 250))

# ---------- CORRECTED GAME PATHS ----------
GAMES = {
    "Riddle Game": {
        "folder": "Riddle game by nadriekoda",
        "file": "game ver 5.py",
        "full_path": r"riddle game/riddler.py"
    },
    "Marble Game": {
        "folder": "marbble game",
        "file": "marble.py",
        "full_path": r"marbble game/marble.py"
    },
    "Nyama Nyama": {
        "folder": "Nyama Nyama",
        "file": "Nyama ver 2.py",
        "full_path": r"Nyama Nyama/Nyama ver 2.py"
    }
}

# ---------- BUTTONS ----------
buttons = {
    "Riddle Game": pygame.Rect(250, 150, 300, 60),
    "Marble Game": pygame.Rect(250, 230, 300, 60),
    "Nyama Nyama": pygame.Rect(250, 310, 300, 60),
    "About Us": pygame.Rect(250, 390, 300, 60),
    "Quit": pygame.Rect(250, 470, 300, 60)
}

# About button for top-right corner
about_button_rect = pygame.Rect(WIDTH - 50, 20, 30, 30)

def check_game_exists(game_name):
    """Check if game file exists"""
    game_info = GAMES.get(game_name)
    if not game_info:
        return False, None
    
    # Try multiple approaches:
    paths_to_check = [
        game_info["full_path"],
        os.path.join(game_info["folder"], game_info["file"]),
        game_info["file"]
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            return True, path
    
    # Check folder and look for any Python file
    folder_path = game_info["folder"]
    if os.path.exists(folder_path):
        try:
            files = os.listdir(folder_path)
            for filename in files:
                if filename.lower().endswith('.py'):
                    # Check for game name keywords
                    game_lower = game_name.lower()
                    filename_lower = filename.lower()
                    
                    if "marble" in game_lower and "marble" in filename_lower:
                        found_path = os.path.join(folder_path, filename)
                        return True, found_path
                    elif "riddle" in game_lower and ("riddle" in filename_lower or "game" in filename_lower):
                        found_path = os.path.join(folder_path, filename)
                        return True, found_path
                    elif "nyama" in game_lower and "nyama" in filename_lower:
                        found_path = os.path.join(folder_path, filename)
                        return True, found_path
                    elif "ver" in filename_lower:
                        found_path = os.path.join(folder_path, filename)
                        return True, found_path
            
            # If no keyword match, return first Python file
            py_files = [f for f in files if f.lower().endswith('.py')]
            if py_files:
                first_py = os.path.join(folder_path, py_files[0])
                return True, first_py
        except:
            pass
    
    return False, None

def launch_game(game_name):
    """Launch a game with the correct file name"""
    exists, game_path = check_game_exists(game_name)
    
    if not exists:
        print(f"\n ERROR: {game_name} not found!")
        print(f"Looking for: {GAMES[game_name]['file']}")
        print(f"In folder: {GAMES[game_name]['folder']}")
        return False
    
    print(f"\n{'='*60}")
    print(f" LAUNCHING: {game_name}")
    print(f" Path: {game_path}")
    print(f" Folder: {os.path.dirname(game_path)}")
    print(f" File: {os.path.basename(game_path)}")
    print(f"{'='*60}")
    
    try:
        game_dir = os.path.dirname(game_path)
        game_file = os.path.basename(game_path)
        
        print(f"Method: Running in game's directory")
        print(f"Directory: {game_dir}")
        print(f"Command: python {game_file}")
        
        # Change to game directory and run
        original_dir = os.getcwd()
        try:
            os.chdir(game_dir)
            result = subprocess.run([sys.executable, game_file], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=30)
            
            if result.returncode == 0:
                print(f" {game_name} finished successfully!")
            else:
                print(f"⚠ {game_name} exited with code: {result.returncode}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                if result.stderr:
                    print(f"Errors: {result.stderr}")
                    
        except subprocess.TimeoutExpired:
            print(f" {game_name} timed out after 30 seconds")
        finally:
            os.chdir(original_dir)
        
        print(f"{'='*60}\n")
        return True
        
    except Exception as e:
        print(f" Error launching {game_name}: {type(e).__name__}: {e}")
        
        # Try alternative method with os.system
        print("\nTrying alternative launch method...")
        try:
            command = f'python "{game_path}"'
            print(f"Command: {command}")
            result = os.system(command)
            
            if result == 0:
                print(f" {game_name} finished successfully!")
            else:
                print(f"⚠ {game_name} exited with code: {result}")
        except Exception as e2:
            print(f" Alternative method also failed: {e2}")
        
        print(f"{'='*60}\n")
        return False

def draw_button(screen, rect, text, hover=False, exists=True):
    """Draw a button with visual feedback"""
    if not exists:
        color = (150, 150, 150)
        border_color = (100, 100, 100)
        text_color = (100, 100, 100)
    elif hover:
        if text == "Quit":
            color = HOVER_RED
        elif text == "About Us":
            color = HOVER_PURPLE
        elif text == "Nyama Nyama":
            color = HOVER_PURPLE
        else:
            color = HOVER_GREEN
        border_color = BLACK
        text_color = BLACK
    else:
        if text == "Quit":
            color = RED
        elif text == "About Us":
            color = PURPLE
        elif text == "Nyama Nyama":
            color = PURPLE
        else:
            color = GREEN
        border_color = BLACK
        text_color = BLACK
    
    # Draw button
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, border_color, rect, 3, border_radius=12)
    
    # Draw text
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    
    # Draw status indicator for game buttons only
    if text not in ["Quit", "About Us"]:
        status = "✓" if exists else "✗"
        status_color = GREEN if exists else RED
        status_surface = font.render(status, True, status_color)
        screen.blit(status_surface, (rect.right - 40, rect.centery - 15))

def draw_debug_info(screen):
    """Draw debug information"""
    debug_y = 540  # Moved to bottom
    small_font = pygame.font.Font(None, 28)
    
    for game_name in ["Riddle Game", "Marble Game", "Nyama Nyama"]:
        exists, path = check_game_exists(game_name)
        
        # Draw game status
        if exists:
            filename = os.path.basename(path)
            # Color coding for different games
            if game_name == "Nyama Nyama":
                color = PURPLE
            else:
                color = GREEN
            status_text = small_font.render(f"✓ {game_name}: {filename}", True, color)
        else:
            status_text = small_font.render(f"✗ {game_name}: Not Found", True, RED)
        
        # Center the status text
        text_rect = status_text.get_rect(center=(WIDTH//2, debug_y))
        screen.blit(status_text, text_rect)
        debug_y += 25

def draw_menu():
    """Draw the main menu screen"""
    screen.blit(image, (0, 0))
    
    # Draw title with version
    title = font.render("AFRI PLAY", True, BLUE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw subtitle
    subtitle = small_font.render("Now with Nyama Nyama Game!", True, DARK_GRAY)
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 75))
    
    # Draw buttons with hover effects
    mouse_pos = pygame.mouse.get_pos()
    
    for text, rect in buttons.items():
        if text not in ["Quit", "About Us"]:
            exists, _ = check_game_exists(text)
            hover = rect.collidepoint(mouse_pos)
            draw_button(screen, rect, text, hover, exists)
        else:
            hover = rect.collidepoint(mouse_pos)
            draw_button(screen, rect, text, hover, True)
    
    # Draw debug information
    draw_debug_info(screen)
    
  

def draw_about():
    """Draw the about us screen"""
    
    about_img=pygame.transform.scale(pygame.image.load("Launcher assets/about us.png"), (WIDTH, HEIGHT))
    # Draw back button
    back_button = pygame.Rect(20, 20, 100, 40)
    mouse_pos = pygame.mouse.get_pos()
    hover_back = back_button.collidepoint(mouse_pos)
    
    back_color = HOVER_PURPLE if hover_back else PURPLE
    pygame.draw.rect(screen, back_color, back_button, border_radius=8)
    pygame.draw.rect(screen, WHITE, back_button, 2, border_radius=8)
    
    back_text = small_font.render("← Back", True, WHITE)
    screen.blit(back_text, (back_button.centerx - back_text.get_width()//2, 
                           back_button.centery - back_text.get_height()//2))
    screen.blit(about_image, (0, 0))
    # Draw instructions for adding custom image
    if "fallback" in str(about_image):  # If using fallback image
        instruction_font = pygame.font.Font(None, 24)
        instruction1 = instruction_font.render("To add your own About Us image:", True, YELLOW)
        instruction2 = instruction_font.render("1. Save image as 'Launcher assets/about_us.png'", True, WHITE)
        instruction3 = instruction_font.render("2. Restart the launcher", True, WHITE)
        
        screen.blit(instruction1, (WIDTH//2 - instruction1.get_width()//2, 350))
        screen.blit(instruction2, (WIDTH//2 - instruction2.get_width()//2, 380))
        screen.blit(instruction3, (WIDTH//2 - instruction3.get_width()//2, 410))
    
    return back_button

# ---------- INITIAL CHECK ----------
print("\n" + "="*70)
print("GAME LAUNCHER - INITIAL CHECK")
print("="*70)
print(f"Current directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print()

# Check all paths
for game_name in ["Riddle Game", "Marble Game", "Nyama Nyama"]:
    exists, path = check_game_exists(game_name)
    status = " FOUND" if exists else " NOT FOUND"
    print(f"{game_name}: {status}")

    
    if exists:
        print(f"  Path: {path}")
        print(f"  File: {os.path.basename(path)}")
        print(f"  Folder: {os.path.dirname(path)}")
    else:
        print(f"  Looking for: {GAMES[game_name]['file']}")
        print(f"  In folder: {GAMES[game_name]['folder']}")
        
        # Check what's actually in the folder
        folder_path = GAMES[game_name]["folder"]
        if os.path.exists(folder_path):
            print(f"  Folder exists! Contents:")
            try:
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        print(f"     {item} ({size} bytes)")
                    else:
                        print(f"     {item}/")
            except Exception as e:
                print(f"    Error: {e}")
        else:
            print(f"  Folder doesn't exist at: {folder_path}")
    
    print()

print("="*70)
print("Click buttons to launch games (check console for output)")
print("="*70 + "\n")

# ---------- MAIN LOOP ----------
running = True
back_button = None  # Initialize back button

while running:
    
    if current_state == MENU:
        draw_menu()
    elif current_state == ABOUT:
        back_button = draw_about()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if current_state == MENU:
                # Check game buttons
                for text, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if text == "Quit":
                            running = False
                        elif text == "About Us":
                            current_state = ABOUT
                        else:
                            exists, _ = check_game_exists(text)
                            if exists:
                                launch_game(text)
                            else:
                                print(f"\n⚠ Cannot launch {text}!")
                                print(f"File '{GAMES[text]['file']}' not found in '{GAMES[text]['folder']}'")
                                print("Please check the file name is correct!\n")
            
            elif current_state == ABOUT:
                screen.blit(about_image, (0, 0))
                # Check back button
                if back_button and back_button.collidepoint(mouse_pos):
                    current_state = MENU
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
print("\n" + "="*70)
print("Game Launcher closed")
print("="*70)