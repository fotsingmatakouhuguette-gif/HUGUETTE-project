import pygame
import math
import array

def tone(freq, duration):
    rate = 44100
    n = int(rate * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / rate
        buf.append(int(32767 * math.sin(2 * math.pi * freq * t)))
    return pygame.mixer.Sound(buffer=buf)

sound_good = tone(700, 0.2)
sound_bad = tone(200, 0.3)