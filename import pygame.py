import pygame
import sys
import os 
from pygame import gfxdraw 
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mystery Riddle Challenge")
COLORS = {
    'bg': (30, 30, 46),           
    'panel': (44, 44, 64),        
    'accent': (103, 89, 217),   
    'secondary': (88, 166, 255),  
    'text': (248, 248, 242),      
    'correct': (80, 250, 123),    
    'wrong': (255, 85, 85),      
    'hint': (255, 184, 108),      
    'border': (68, 71, 90),       
}
def load_fonts():
    fonts = {
        'title': pygame.font.Font(None, 64),
        'subtitle': pygame.font.Font(None, 36),
        'normal': pygame.font.Font(None, 32),
        'small': pygame.font.Font(None, 24),
        'mono': pygame.font.SysFont('couriernew', 28)
    }
    return fonts

fonts = load_fonts()
def rounded_rect(surface, rect, color, radius=20, border=0, border_color=None):
    x, y, width, height = rect
    rect_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.gfxdraw.aacircle(rect_surf, radius, radius, radius, color)
    pygame.gfxdraw.filled_circle(rect_surf, radius, radius, radius, color)
    pygame.gfxdraw.aacircle(rect_surf, width - radius - 1, radius, radius, color)
    pygame.gfxdraw.filled_circle(rect_surf, width - radius - 1, radius, radius, color)
    pygame.gfxdraw.aacircle(rect_surf, radius, height - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(rect_surf, radius, height - radius - 1, radius, color)
    pygame.gfxdraw.aacircle(rect_surf, width - radius - 1, height - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(rect_surf, width - radius - 1, height - radius - 1, radius, color)
    pygame.draw.rect(rect_surf, color, (radius, 0, width - 2 * radius, height))
    pygame.draw.rect(rect_surf, color, (0, radius, width, height - 2 * radius))
    
    if border > 0 and border_color:
        pygame.gfxdraw.aacircle(rect_surf, radius, radius, radius, border_color)
        pygame.gfxdraw.aacircle(rect_surf, width - radius - 1, radius, radius, border_color)
        pygame.gfxdraw.aacircle(rect_surf, radius, height - radius - 1, radius, border_color)
        pygame.gfxdraw.aacircle(rect_surf, width - radius - 1, height - radius - 1, radius, border_color)
        pygame.draw.rect(rect_surf, border_color, (radius, 0, width - 2 * radius, border))
        pygame.draw.rect(rect_surf, border_color, (radius, height - border, width - 2 * radius, border))
        pygame.draw.rect(rect_surf, border_color, (0, radius, border, height - 2 * radius))
        pygame.draw.rect(rect_surf, border_color, (width - border, radius, border, height - 2 * radius))
    
    surface.blit(rect_surf, (x, y))

class Button:
    def __init__(self, x, y, width, height, text, color=COLORS['accent'], hover_color=COLORS['secondary']):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.clicked = False
        
    def draw(self, surface):
        rounded_rect(surface, self.rect, self.current_color, radius=15, border=2, border_color=COLORS['border'])
        
        text_surf = fonts['normal'].render(self.text, True, COLORS['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
        if self.is_hovered:
            pygame.draw.rect(surface, (255, 255, 255, 30), self.rect, 2, border_radius=15)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        return self.is_hovered
    
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                self.clicked = True
                return True
        return False

class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, surface):
        rounded_rect(surface, self.rect, COLORS['panel'], radius=12, border=2, 
                    border_color=COLORS['accent'] if self.active else COLORS['border'])
        
        if self.text:
            text_surf = fonts['mono'].render(self.text, True, COLORS['text'])
            surface.blit(text_surf, (self.rect.x + 15, self.rect.centery - text_surf.get_height() // 2))
        else:
            placeholder = fonts['small'].render("Type your answer here...", True, (150, 150, 150))
            surface.blit(placeholder, (self.rect.x + 15, self.rect.centery - placeholder.get_height() // 2))
        if self.active and self.cursor_visible:
            text_width = fonts['mono'].size(self.text)[0] if self.text else 0
            cursor_x = self.rect.x + 15 + text_width
            pygame.draw.line(surface, COLORS['text'], 
                           (cursor_x, self.rect.y + 10),
                           (cursor_x, self.rect.y + self.rect.height - 10), 2)
    
    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 30: 
                    self.text += event.unicode
        return None

def draw_riddle_card(surface, riddle_text, riddle_number, total_riddles, category):
    card_rect = (50, 120, SCREEN_WIDTH - 100, 300)
    rounded_rect(surface, card_rect, COLORS['panel'], radius=25, border=3, border_color=COLORS['accent'])
    header_rect = (card_rect[0], card_rect[1], card_rect[2], 60)
    rounded_rect(surface, header_rect, COLORS['accent'], radius=25, border=0)
    category_bg = (card_rect[0] + 30, card_rect[1] + 75, 150, 40)
    rounded_rect(surface, category_bg, COLORS['secondary'], radius=10)
    category_text = fonts['small'].render(category.upper(), True, COLORS['text'])
    surface.blit(category_text, (category_bg[0] + 20, category_bg[1] + 10))
    progress_text = fonts['normal'].render(f"Riddle {riddle_number}/{total_riddles}", True, COLORS['text'])
    surface.blit(progress_text, (card_rect[0] + card_rect[2] - 200, card_rect[1] + 20))
    words = riddle_text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if fonts['normal'].size(test_line)[0] < card_rect[2] - 100:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    for i, line in enumerate(lines):
        line_surf = fonts['normal'].render(line, True, COLORS['text'])
        surface.blit(line_surf, (card_rect[0] + 50, card_rect[1] + 130 + i * 40))

    pygame.draw.circle(surface, COLORS['accent'], (card_rect[0] + 20, card_rect[1] + 150), 8)
    pygame.draw.circle(surface, COLORS['secondary'], (card_rect[0] + card_rect[2] - 20, card_rect[1] + 150), 8)

def draw_stats_panel(surface, score, hints_remaining, time_remaining):
    panel_rect = (50, 450, SCREEN_WIDTH - 100, 80)
    rounded_rect(surface, panel_rect, COLORS['panel'], radius=20, border=2, border_color=COLORS['border'])
    
    score_text = fonts['subtitle'].render(f"Score: {score}", True, COLORS['correct'])
    surface.blit(score_text, (panel_rect[0] + 30, panel_rect[1] + 25))
    hint_text = fonts['normal'].render(f"Hints: {hints_remaining}", True, COLORS['hint'])
    surface.blit(hint_text, (panel_rect[0] + 250, panel_rect[1] + 30))
    for i in range(3):
        hint_color = COLORS['hint'] if i < hints_remaining else (100, 100, 100)
        pygame.draw.circle(surface, hint_color, (panel_rect[0] + 350 + i * 35, panel_rect[1] + 40), 10)
    time_color = COLORS['text'] if time_remaining > 10 else COLORS['wrong']
    timer_text = fonts['normal'].render(f"Time: {time_remaining}s", True, time_color)
    surface.blit(timer_text, (panel_rect[0] + panel_rect[2] - 150, panel_rect[1] + 30))

class FeedbackAnimation:
    def __init__(self):
        self.messages = []
        self.duration = 120  
        
    def add_message(self, message, color):
        self.messages.append({
            'text': message,
            'color': color,
            'timer': self.duration,
            'y': SCREEN_HEIGHT - 100
        })
    
    def update(self):
        for msg in self.messages[:]:
            msg['timer'] -= 1
            msg['y'] -= 1 
            if msg['timer'] <= 0:
                self.messages.remove(msg)
    
    def draw(self, surface):
        for msg in self.messages:
            alpha = min(255, msg['timer'] * 2)
            text_surf = fonts['normal'].render(msg['text'], True, msg['color'])
            text_surf.set_alpha(alpha)
            surface.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, msg['y']))

class RiddleGame:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.hints = 3
        self.current_riddle = 0
        self.feedback = FeedbackAnimation()
        self.riddles = [
            {
                'question': 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?',
                'answer': 'echo',
                'category': 'Nature',
                'hints': ['It repeats what you say', 'Found in mountains', 'Sound reflection']
            },
            {
                'question': 'The more you take, the more you leave behind. What am I?',
                'answer': 'footsteps',
                'category': 'Logic',
                'hints': ['Related to walking', 'They follow you', 'Impression makers']
            }
        ]
        self.input_box = InputBox(50, 550, SCREEN_WIDTH - 200, 50)
        self.submit_btn = Button(SCREEN_WIDTH - 130, 550, 80, 50, "Submit")
        self.hint_btn = Button(50, 620, 120, 50, "Hint")
        self.skip_btn = Button(200, 620, 120, 50, "Skip")
        self.time_limit = 60 
        self.start_time = pygame.time.get_ticks()
    
    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            color_value = 30 + (y / SCREEN_HEIGHT) * 10
            pygame.draw.line(self.screen, (color_value, color_value, color_value + 16), 
                           (0, y), (SCREEN_WIDTH, y))
        for i in range(20):
            x = (i * 100) % SCREEN_WIDTH
            y = (i * 50) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, (40, 40, 60, 50), (x, y), 30, 1)
    def draw_header(self):
        title = fonts['title'].render("RIDDLE QUEST", True, COLORS['text'])
        shadow = fonts['title'].render("RIDDLE QUEST", True, (0, 0, 0, 100))
        
        self.screen.blit(shadow, (53, 53))
        self.screen.blit(title, (50, 50))
        subtitle = fonts['small'].render("Can you solve them all?", True, COLORS['secondary'])
        self.screen.blit(subtitle, (50, 110))
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            result = self.input_box.handle_event(event)
            if result is not None:
                self.check_answer(result)
            if self.submit_btn.check_click(mouse_pos, event):
                self.check_answer(self.input_box.text)
            
            if self.hint_btn.check_click(mouse_pos, event):
                self.use_hint()
            
            if self.skip_btn.check_click(mouse_pos, event):
                self.skip_riddle()
            self.submit_btn.check_hover(mouse_pos)
            self.hint_btn.check_hover(mouse_pos)
            self.skip_btn.check_hover(mouse_pos)
    
    def check_answer(self, answer):
        current = self.riddles[self.current_riddle]
        if answer.lower() == current['answer'].lower():
            self.score += 10
            self.feedback.add_message("✅ Correct! +10 points", COLORS['correct'])
            self.next_riddle()
        else:
            self.feedback.add_message("❌ Try again!", COLORS['wrong'])
    
    def use_hint(self):
        if self.hints > 0:
            self.hints -= 1
            current = self.riddles[self.current_riddle]
            hint_index = 3 - self.hints - 1
            if hint_index < len(current['hints']):
                self.feedback.add_message(f"💡 Hint: {current['hints'][hint_index]}", COLORS['hint'])
        else:
            self.feedback.add_message("No hints remaining!", COLORS['wrong'])
    
    def skip_riddle(self):
        self.feedback.add_message("⏩ Riddle skipped", COLORS['text'])
        self.next_riddle()
    
    def next_riddle(self):
        self.input_box.text = ""
        self.current_riddle = (self.current_riddle + 1) % len(self.riddles)
        self.start_time = pygame.time.get_ticks()
    
    def calculate_time_remaining(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        return max(0, self.time_limit - elapsed)
    
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.input_box.update()
            self.feedback.update()
            if self.calculate_time_remaining() == 0:
                self.feedback.add_message("⏰ Time's up!", COLORS['wrong'])
                self.next_riddle()
            self.handle_events()
            self.draw_background()
            self.draw_header()
            
            if self.current_riddle < len(self.riddles):
                current = self.riddles[self.current_riddle]
                draw_riddle_card(self.screen, current['question'], 
                               self.current_riddle + 1, len(self.riddles), 
                               current['category'])
            
            draw_stats_panel(self.screen, self.score, self.hints, 
                           self.calculate_time_remaining())
            
            self.input_box.draw(self.screen)
            self.submit_btn.draw(self.screen)
            self.hint_btn.draw(self.screen)
            self.skip_btn.draw(self.screen)
            self.feedback.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RiddleGame()
    game.run()
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Riddle Game",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/riddle_game.py",
            "console": "integratedTerminal"
        }
    ]
}
