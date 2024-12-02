import random
from datetime import datetime
from random import randrange

import pygame

from Source.assets import AssetManager
from Source.config import LEVEL_BOUND_PX_SIZE


def get_upper_bound(screen) -> int:
    return screen.get_height() - LEVEL_BOUND_PX_SIZE

def get_lower_bound() -> int:
    return LEVEL_BOUND_PX_SIZE

def draw_bounds(screen):
    bound = AssetManager.get_sprite("panel")
    size_value = min(screen.get_width(), get_lower_bound())
    accumulated = 0
    while accumulated < screen.get_width():
        bound = pygame.transform.scale(bound, (size_value, size_value))
        screen.blit(bound, (accumulated, 0))
        screen.blit(bound, (accumulated, get_upper_bound(screen)))
        accumulated += bound.get_height()

last_wall_effect_change = datetime.now()
current_effect = "fire1"

def draw_death_wall(screen):
    global last_wall_effect_change, current_effect

    if (datetime.now() - last_wall_effect_change).total_seconds() > 0.2:
        current_effect = random.choice(["fire1", "fire2", "fire3", "fire4"])
        last_wall_effect_change = datetime.now()

    wall = AssetManager.get_sprite(current_effect)
    wall = pygame.transform.rotate(wall, -90)
    wall.set_alpha(255)
    size_value = 50
    accumulated = 0
    while accumulated < screen.get_height():
        wall = pygame.transform.scale(wall, (size_value, size_value))
        screen.blit(wall, (0, accumulated))
        accumulated += wall.get_height()

def get_random_height_pos(screen):
    return randrange(get_lower_bound(), get_upper_bound(screen))