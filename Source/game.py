from datetime import datetime

import pygame
from pygame import Vector2

from Source.assets import AssetManager
from Source.config import PLAYER_FUEL_REGEN, PLAYER_FUEL_MAX, LEVEL_GEN_EARTH_SIZE
from Source.decorative_object import DecorativeObject
from Source.gravitation_object import GravitationObject
from Source.player import Player
from Source.score import register_score
from Source.scoring import apply_score_for_one_planet

player: Player | None = None
gravitation_objects:list[GravitationObject] = []
decorative_objects:list[DecorativeObject] = []
score = 0
fuel = PLAYER_FUEL_MAX
death_time: datetime | None = None
game_finished = False

def reset_game(screen):
    global score, fuel, game_finished, death_time, decorative_objects, gravitation_objects, player
    player = Player()
    player.position = Vector2(screen.get_width() - LEVEL_GEN_EARTH_SIZE * 2, screen.get_height() / 2)
    gravitation_objects = []
    decorative_objects = []
    score = 0
    fuel = PLAYER_FUEL_MAX
    death_time = None
    game_finished = False

def try_finish_game():
    if (datetime.now() - death_time).total_seconds() > 5:
        register_score(score)

        global game_finished
        game_finished = True

def use_fuel(used: float):
    global fuel
    fuel -= used
    fuel = max(fuel, 0)

def regen_fuel():
    global fuel
    fuel += PLAYER_FUEL_REGEN
    fuel = min(fuel, PLAYER_FUEL_MAX)

def get_level_move_speed() -> float:
    if death_time is not None:
        delta_seconds = (datetime.now() - death_time).total_seconds()

        death_coef = 1 - min(1.0, delta_seconds / 5)
    else:
        death_coef = 1

    return -150 if death_time is None else -150 * death_coef

def tick_physics(dt):

    move_offset = Vector2(get_level_move_speed() * dt, 0)

    for gravitation_object in gravitation_objects:
        gravitation_object.position += move_offset

        if gravitation_object.position.x < -gravitation_object.size:
            gravitation_objects.pop(gravitation_objects.index(gravitation_object))
            apply_score_for_one_planet()

    if player.is_landed:
        player.position += move_offset
        regen_fuel()

def master_init():
    pygame.init()
    AssetManager.collect_assets()
    pygame.mixer.init()
