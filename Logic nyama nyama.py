import random
import time
from data import categories

def new_round():
    category, items = random.choice(categories)
    word, value = random.choice(list(items.items()))
    return category, word, value

def level_time(level):
    if level == 1:
        return 8
    if level == 2:
        return 5
    return 3