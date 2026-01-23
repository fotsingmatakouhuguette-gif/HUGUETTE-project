import pygame
import math
import random
import json
import sys

# Initialize Pygame
pygame.init()

# ==================== CONFIGURATION ====================
# Get full screen dimensions
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GRAY = (128, 128, 128)

# ==================== MARBLE GAME CLASSES ====================
class Marble:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.color = color
        self.radius = int(15 * (min(WIDTH, HEIGHT) / 900))  # Scale with screen size
        self.friction = 0.98

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dx *= self.friction
        self.dy *= self.friction
        if abs(self.dx) < 0.1: self.dx = 0
        if abs(self.dy) < 0.1: self.dy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 1)

class MarbleGame:
    def __init__(self, screen):
        self.screen = screen
        self.font_size = max(26, int(26 * (min(WIDTH, HEIGHT) / 900)))
        self.font = pygame.font.SysFont("Arial", self.font_size, bold=True)
        self.reset()
        
    def reset(self):
        self.state = "name_entry"
        self.player_names = ["", ""]
        self.name_idx = 0
        
    def get_player_names(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_RETURN and self.player_names[self.name_idx]:
                    self.name_idx += 1
                    if self.name_idx > 1:
                        self.setup_game()
                        return None
                elif event.key == pygame.K_BACKSPACE:
                    self.player_names[self.name_idx] = self.player_names[self.name_idx][:-1]
                elif len(event.unicode) > 0 and event.unicode.isprintable():
                    self.player_names[self.name_idx] += event.unicode
        
        self.screen.fill(BLACK)
        prompt = self.font.render(f"Player {self.name_idx+1} Name: {self.player_names[self.name_idx]}_", True, WHITE)
        self.screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
        
        esc_text = self.font.render("Press ESC to return to menu", True, GRAY)
        self.screen.blit(esc_text, (WIDTH//2 - esc_text.get_width()//2, HEIGHT-50))
        return None
        
    def setup_game(self):
        self.state = "playing"
        self.center_ring = (WIDTH // 2, HEIGHT // 2 - 30)
        self.ring_r = int(130 * (min(WIDTH, HEIGHT) / 900))
        self.line_y = HEIGHT - int(120 * (HEIGHT / 750))
        self.shoot_pos = (WIDTH // 2, self.line_y)
        
        self.p_marbles = [4, 4]
        self.collected = [0, 0]
        self.current_p = 0
        self.targets = [Marble(self.center_ring[0]+random.randint(-50,50), 
                              self.center_ring[1]+random.randint(-50,50), GOLD) for _ in range(6)]
        
        self.shooter = Marble(self.shoot_pos[0], self.shoot_pos[1], 
                             RED if self.current_p == 0 else BLUE)
        self.is_charging = False
        self.moving = False
        self.hit_this_turn = False
        
    def resolve_collision(self, m1, m2):
        dx, dy = m2.x - m1.x, m2.y - m1.y
        dist = math.hypot(dx, dy)
        if dist < m1.radius * 2 and dist > 0:
            overlap = m1.radius * 2 - dist
            m1.x -= overlap * (dx/dist) * 0.5
            m1.y -= overlap * (dy/dist) * 0.5
            m1.dx, m2.dx = m2.dx, m1.dx
            m1.dy, m2.dy = m2.dy, m1.dy
            return True
        return False
        
    def run(self):
        if self.state == "name_entry":
            return self.get_player_names()
        elif self.state == "playing":
            return self.play_game()
        elif self.state == "game_over":
            return self.show_winner()
            
    def play_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
                
            if not self.moving and self.p_marbles[self.current_p] > 0:
                mx, my = pygame.mouse.get_pos()
                dist = math.hypot(mx - self.shooter.x, my - self.shooter.y)
                if event.type == pygame.MOUSEBUTTONDOWN and dist < self.shooter.radius * 2:
                    self.is_charging = True
                if event.type == pygame.MOUSEBUTTONUP and self.is_charging:
                    self.shooter.dx = (self.shooter.x - mx) * 0.16
                    self.shooter.dy = (self.shooter.y - my) * 0.16
                    self.is_charging = False
                    self.moving = True
                    self.hit_this_turn = False
        
        if self.moving:
            self.shooter.move()
            for t in self.targets[:]:
                t.move()
                if self.resolve_collision(self.shooter, t):
                    self.targets.remove(t)
                    self.collected[self.current_p] += 1
                    self.hit_this_turn = True
                
                if math.hypot(t.x - self.center_ring[0], t.y - self.center_ring[1]) > self.ring_r:
                    if t in self.targets:
                        self.targets.remove(t)
                        self.collected[self.current_p] += 1
                        self.hit_this_turn = True
            
            if self.shooter.dx == 0 and self.shooter.dy == 0 and all(t.dx == 0 for t in self.targets):
                if self.hit_this_turn:
                    self.collected[self.current_p] += 1
                else:
                    if math.hypot(self.shooter.x - self.center_ring[0], 
                                 self.shooter.y - self.center_ring[1]) < self.ring_r:
                        self.shooter.color = GOLD
                        self.targets.append(self.shooter)
                        self.p_marbles[self.current_p] -= 1
                    
                    self.current_p = 1 - self.current_p
                
                self.moving = False
                self.shooter = Marble(self.shoot_pos[0], self.shoot_pos[1], 
                                     RED if self.current_p == 0 else BLUE)
        
        # Draw
        self.screen.fill(GREEN)
        pygame.draw.circle(self.screen, WHITE, self.center_ring, self.ring_r, 3)
        pygame.draw.line(self.screen, WHITE, (0, self.line_y - 30), 
                        (WIDTH, self.line_y - 30), 4)
        
        # UI
        p1_info = self.font.render(f"{self.player_names[0]} | Ammo: {self.p_marbles[0]} | Wins: {self.collected[0]}", 
                                   True, RED)
        p2_info = self.font.render(f"{self.player_names[1]} | Ammo: {self.p_marbles[1]} | Wins: {self.collected[1]}", 
                                   True, BLUE)
        self.screen.blit(p1_info, (20, 20))
        self.screen.blit(p2_info, (WIDTH - p2_info.get_width() - 20, 20))
        
        turn_txt = self.font.render(f"{self.player_names[self.current_p]}'s TURN", True, WHITE)
        self.screen.blit(turn_txt, (WIDTH//2 - turn_txt.get_width()//2, 60))
        
        for i in range(self.p_marbles[0]):
            pygame.draw.circle(self.screen, RED, (30, HEIGHT - 30 - (i*25)), 10)
        for i in range(self.p_marbles[1]):
            pygame.draw.circle(self.screen, BLUE, (WIDTH - 30, HEIGHT - 30 - (i*25)), 10)
        
        mx, my = pygame.mouse.get_pos()
        if self.is_charging:
            pygame.draw.line(self.screen, WHITE, (self.shooter.x, self.shooter.y), (mx, my), 2)
        if not self.moving or self.shooter.dx != 0:
            self.shooter.draw(self.screen)
        for t in self.targets:
            t.draw(self.screen)
        
        esc_text_font = pygame.font.Font(None, int(20 * (min(WIDTH, HEIGHT) / 900)))
        esc_text = esc_text_font.render("ESC: Menu", True, WHITE)
        self.screen.blit(esc_text, (10, HEIGHT-30))
        
        if self.p_marbles[0] <= 0 or self.p_marbles[1] <= 0 or len(self.targets) == 0:
            self.state = "game_over"
        
        return None
        
    def show_winner(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                return "menu"
        
        self.screen.fill(BLACK)
        win_idx = 0 if self.collected[0] > self.collected[1] else 1
        msg = f"{self.player_names[win_idx]} WINS WITH {self.collected[win_idx]} MARBLES!"
        win_text = self.font.render(msg, True, GOLD)
        self.screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
        
        continue_text = self.font.render("Press any key to continue", True, WHITE)
        self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2+50))
        
        return None

# ==================== RIDDLE GAME ====================
class RiddleGame:
    def __init__(self, screen):
        self.screen = screen
        self.base_font_size = 36
        self.scale_factor = min(WIDTH, HEIGHT) / 900
        self.font = pygame.font.Font(None, int(self.base_font_size * self.scale_factor))
        self.big_font = pygame.font.Font(None, int(64 * self.scale_factor))
        self.small_font = pygame.font.Font(None, int(24 * self.scale_factor))
        
        # Embedded riddles
        self.riddles = [
            {"question": "The more you move, the more you leave behind", "choices": {"1": "Shadow", "2": "Footstep", "3": "Wind", "4": "Dust"}, "answer": 2},
            {"question": "I have cities but no houses, water but no fishes, and mountains but no trees. Who am I?", "choices": {"1": "Globe", "2": "Painting", "3": "Map", "4": "Dream"}, "answer": 3},
            {"question": "I disappear as soon as they call my name", "choices": {"1": "Silence", "2": "Echo", "3": "Shadow", "4": "Secret"}, "answer": 1},
            {"question": "What has to be broken before you can use it?", "choices": {"1": "Egg", "2": "Glass", "3": "Stick", "4": "Seal"}, "answer": 1},
            {"question": "I'm born tall and I die short", "choices": {"1": "Tree", "2": "Pencil", "3": "Building", "4": "Candle"}, "answer": 4},
            {"question": "I get wetter the more I dry. Who am I?", "choices": {"1": "Sponge", "2": "Cloud", "3": "Rain", "4": "Towel"}, "answer": 4},
            {"question": "What word is spelled incorrectly in all dictionaries?", "choices": {"1": "Wrong", "2": "Incorrectly", "3": "Mistake", "4": "Error"}, "answer": 2},
            {"question": "I have keys but no room. Who am I?", "choices": {"1": "Piano", "2": "Keyboard", "3": "Lock", "4": "Map"}, "answer": 2},
            {"question": "Forward I was heavy, backward I'm not. What am I?", "choices": {"1": "Load", "2": "Weight", "3": "Ton / Not", "4": "Stone"}, "answer": 3},
            {"question": "The more you have of me, the less you see", "choices": {"1": "Fog", "2": "Darkness", "3": "Night", "4": "Smoke"}, "answer": 2}
        ]
        
        self.GROUND_LEVEL = int(430 * (HEIGHT / 750))
        self.GRAVITY = 1
        self.JUMP_FORCE = -22
        self.MAX_LIVES = 3
        self.RIDDLE_TIME = 30
        
        self.reset()
        
    def reset(self):
        self.state = "playing"
        self.lives = self.MAX_LIVES
        self.start_time = pygame.time.get_ticks()
        
        self.player_rect = pygame.Rect(int(100 * (WIDTH / 900)), self.GROUND_LEVEL - int(50 * (HEIGHT / 750)), 
                                       int(40 * self.scale_factor), int(50 * self.scale_factor))
        self.player_velocity = 0
        self.is_jumping = False
        
        self.enemies = []
        self.flying_enemies = []
        self.enemy_timer = 0
        self.flying_timer = 0
        
        self.current_riddle = None
        self.riddle_start_time = 0
        self.collision_locked = False
        self.riddles_answered = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        
        self.feedback_text = ""
        self.feedback_color = WHITE
        self.feedback_start_time = 0
        self.show_feedback = False
        
    def run(self):
        if self.state == "playing":
            return self.play_game()
        elif self.state == "riddle":
            return self.show_riddle()
        elif self.state == "game_over":
            return self.show_game_over()
        elif self.state == "congrats":
            return self.show_congrats()
            
    def play_game(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE and not self.is_jumping:
                    self.player_velocity = self.JUMP_FORCE
                    self.is_jumping = True
        
        self.player_velocity += self.GRAVITY
        self.player_rect.y += self.player_velocity
        
        if self.player_rect.bottom >= self.GROUND_LEVEL:
            self.player_rect.bottom = self.GROUND_LEVEL
            self.player_velocity = 0
            self.is_jumping = False
        
        self.enemy_timer += 1
        if self.enemy_timer > 120:
            enemy_width = int(40 * self.scale_factor)
            self.enemies.append(pygame.Rect(WIDTH, self.GROUND_LEVEL - enemy_width, enemy_width, enemy_width))
            self.enemy_timer = 0
        
        self.flying_timer += 1
        if self.flying_timer > 180:
            enemy_width = int(40 * self.scale_factor)
            self.flying_enemies.append(pygame.Rect(WIDTH, self.GROUND_LEVEL - int(150 * (HEIGHT / 750)), enemy_width, enemy_width))
            self.flying_timer = 0
        
        for enemy in self.enemies[:]:
            enemy.x -= int(5 * self.scale_factor)
            if enemy.right < 0:
                self.enemies.remove(enemy)
        
        for enemy in self.flying_enemies[:]:
            enemy.x -= int(6 * self.scale_factor)
            if enemy.right < 0:
                self.flying_enemies.remove(enemy)
        
        if not self.collision_locked:
            for enemy in self.enemies + self.flying_enemies:
                if self.player_rect.colliderect(enemy):
                    self.collision_locked = True
                    self.state = "riddle"
                    self.current_riddle = random.choice(self.riddles)
                    self.riddle_start_time = pygame.time.get_ticks()
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    else:
                        self.flying_enemies.remove(enemy)
                    break
        
        self.screen.fill((135, 206, 235))
        pygame.draw.rect(self.screen, (139, 69, 19), (0, self.GROUND_LEVEL, WIDTH, HEIGHT - self.GROUND_LEVEL))
        pygame.draw.rect(self.screen, RED, self.player_rect)
        
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (100, 100, 100), enemy)
        
        for enemy in self.flying_enemies:
            pygame.draw.rect(self.screen, (150, 75, 0), enemy)
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, RED)
        self.screen.blit(lives_text, (20, 20))
        
        time_survived = (current_time - self.start_time) // 1000
        time_text = self.font.render(f"Time: {time_survived}s", True, BLACK)
        self.screen.blit(time_text, (20, 60))
        
        score_text = self.font.render(f"Correct: {self.correct_answers} Wrong: {self.wrong_answers}", True, BLACK)
        self.screen.blit(score_text, (20, 100))
        
        if self.show_feedback and current_time - self.feedback_start_time < 1200:
            feedback = self.font.render(self.feedback_text, True, self.feedback_color)
            self.screen.blit(feedback, (WIDTH//2 - feedback.get_width()//2, 200))
        else:
            self.show_feedback = False
        
        controls_text = self.small_font.render("SPACE: Jump | ESC: Menu", True, BLACK)
        self.screen.blit(controls_text, (10, HEIGHT - 30))
        
        return None
        
    def show_riddle(self):
        current_time = pygame.time.get_ticks()
        time_left = self.RIDDLE_TIME - (current_time - self.riddle_start_time) // 1000
        
        if time_left <= 0:
            self.lives -= 1
            self.riddles_answered += 1
            self.wrong_answers += 1
            self.feedback_text = "Time's up!"
            self.feedback_color = RED
            self.feedback_start_time = pygame.time.get_ticks()
            self.show_feedback = True
            self.collision_locked = False
            
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "playing"
            return None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    choice = int(event.unicode)
                    self.riddles_answered += 1
                    
                    if choice == self.current_riddle["answer"]:
                        self.correct_answers += 1
                        self.feedback_text = "Correct!"
                        self.feedback_color = GREEN
                    else:
                        self.lives -= 1
                        self.wrong_answers += 1
                        self.feedback_text = "Wrong!"
                        self.feedback_color = RED
                    
                    self.feedback_start_time = pygame.time.get_ticks()
                    self.show_feedback = True
                    self.collision_locked = False
                    
                    if self.lives <= 0:
                        self.state = "game_over"
                    elif self.riddles_answered >= 10:
                        self.state = "congrats"
                    else:
                        self.state = "playing"
        
        self.screen.fill((50, 50, 100))
        
        question_lines = self.wrap_text(self.current_riddle["question"], int(700 * self.scale_factor))
        y_offset = int(100 * (HEIGHT / 750))
        for line in question_lines:
            q_text = self.font.render(line, True, WHITE)
            self.screen.blit(q_text, (WIDTH//2 - q_text.get_width()//2, y_offset))
            y_offset += int(40 * self.scale_factor)
        
        y_offset += int(40 * self.scale_factor)
        for key, value in self.current_riddle["choices"].items():
            choice_text = self.font.render(f"{key}. {value}", True, GOLD)
            self.screen.blit(choice_text, (WIDTH//2 - choice_text.get_width()//2, y_offset))
            y_offset += int(50 * self.scale_factor)
        
        timer_text = self.big_font.render(f"{time_left}", True, RED if time_left < 10 else WHITE)
        self.screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, int(50 * (HEIGHT / 750))))
        
        return None
        
    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines
        
    def show_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                return "menu"
        
        self.screen.fill(BLACK)
        
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
        
        stats = self.font.render(f"Correct: {self.correct_answers} | Wrong: {self.wrong_answers}", True, WHITE)
        self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2))
        
        continue_text = self.font.render("Press any key to continue", True, WHITE)
        self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 100))
        
        return None
        
    def show_congrats(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                return "menu"
        
        self.screen.fill((0, 100, 0))
        
        congrats_text = self.big_font.render("CONGRATULATIONS!", True, GOLD)
        self.screen.blit(congrats_text, (WIDTH//2 - congrats_text.get_width()//2, HEIGHT//2 - 100))
        
        stats = self.font.render(f"You completed all riddles!", True, WHITE)
        self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2))
        
        score = self.font.render(f"Correct: {self.correct_answers} | Wrong: {self.wrong_answers}", True, WHITE)
        self.screen.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2 + 50))
        
        continue_text = self.font.render("Press any key to continue", True, WHITE)
        self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 150))
        
        return None

# ==================== MAIN MENU ====================
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, int(72 * (min(WIDTH, HEIGHT) / 900)))
        self.font_medium = pygame.font.Font(None, int(48 * (min(WIDTH, HEIGHT) / 900)))
        
        button_width = int(300 * (WIDTH / 900))
        button_height = int(80 * (HEIGHT / 750))
        button_x = WIDTH//2 - button_width//2
        
        self.marble_button = pygame.Rect(button_x, int(250 * (HEIGHT / 750)), button_width, button_height)
        self.riddle_button = pygame.Rect(button_x, int(360 * (HEIGHT / 750)), button_width, button_height)
        self.quit_button = pygame.Rect(button_x, int(470 * (HEIGHT / 750)), button_width, button_height)
        
    def draw(self):
        self.screen.fill(BLACK)
        
        title = self.font_large.render("WEPLAY", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH//2, int(120 * (HEIGHT / 750))))
        self.screen.blit(title, title_rect)
        
        pygame.draw.rect(self.screen, BLUE, self.marble_button, border_radius=10)
        pygame.draw.rect(self.screen, GREEN, self.riddle_button, border_radius=10)
        pygame.draw.rect(self.screen, RED, self.quit_button, border_radius=10)
        
        marble_text = self.font_medium.render("Marble Game", True, WHITE)
        riddle_text = self.font_medium.render("Riddle Runner", True, WHITE)
        quit_text = self.font_medium.render("Quit", True, WHITE)
        
        self.screen.blit(marble_text, marble_text.get_rect(center=self.marble_button.center))
        self.screen.blit(riddle_text, riddle_text.get_rect(center=self.riddle_button.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
        
    def handle_click(self, pos):
        if self.marble_button.collidepoint(pos):
            return "marble"
        elif self.riddle_button.collidepoint(pos):
            return "riddle"
        elif self.quit_button.collidepoint(pos):
            return "quit"
        return None

# ==================== MAIN ====================
def main():
    # Create full screen display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WePlay - Game Platform")
    clock = pygame.time.Clock()
    
    menu = MainMenu(screen)
    marble_game = None
    riddle_game = None
    
    current_screen = "menu"
    running = True
    
    while running:
        if current_screen == "menu":
            menu.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = menu.handle_click(event.pos)
                    if choice == "marble":
                        marble_game = MarbleGame(screen)
                        current_screen = "marble"
                    elif choice == "riddle":
                        riddle_game = RiddleGame(screen)
                        current_screen = "riddle"
                    elif choice == "quit":
                        running = False
        
        elif current_screen == "marble":
            result = marble_game.run()
            if result == "menu":
                current_screen = "menu"
                marble_game = None
            elif result == "quit":
                running = False
        
        elif current_screen == "riddle":
            result = riddle_game.run()
            if result == "menu":
                current_screen = "menu"
                riddle_game = None
            elif result == "quit":
                running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
