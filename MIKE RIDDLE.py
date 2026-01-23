# --- Configuration & Constants ---
WIDTH, HEIGHT = 800, 600
GROUND_LEVEL = 430
GRAVITY, JUMP_FORCE = 1, -22
MAX_LIVES, RIDDLE_TIME = 3, 30

# --- Load Riddle Data ---
# Ensure your JSON file is in the correct directory
with open("riddles.json", "r", encoding="utf-8") as f:
    riddles = json.load(f)

# --- Sound Initializing ---
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("assets/songs/jump.wav")
hit_sound = pygame.mixer.Sound("assets/songs/hit.wav")
pygame.mixer.music.load("assets/songs/music.mp3")