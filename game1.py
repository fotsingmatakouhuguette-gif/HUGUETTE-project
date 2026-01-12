def load_image(path, size, fallback_color, colorkey=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if colorkey:
            img.set_colorkey(colorkey)
        return pygame.transform.scale(img, size)
    except:
        img = pygame.Surface(size, pygame.SRCALPHA)
        img.fill(fallback_color)
        return img

BACKGROUND_IMAGE = load_image('assets/forestbackground.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), (50, 100, 150))
PLAYER_IMAGE = load_image('assets/player7.png', (60, 80), (255, 0, 0), (255, 255, 255))
ENEMY_IMAGE = load_image('assets/enemy1.png', (50, 70), (0, 255, 0), (255, 255, 255))