from random import randrange

from pygame import Vector2

from Source import game
from Source.config import LEVEL_GEN_EARTH_SIZE
from Source.gravitation_object import GravitationObject
from Source.level_utils import get_random_height_pos


def create_obstacle(screen) -> GravitationObject:
    size_param = randrange(5,20)
    new = GravitationObject(Vector2(screen.get_width(), get_random_height_pos(screen)), size_param, size_param*2.5)

    return new

def try_generating_new_obstacle(screen):
    if len(game.gravitation_objects) == 0:
        game.gravitation_objects.append(
            GravitationObject(Vector2(screen.get_width(), screen.get_height() / 2), LEVEL_GEN_EARTH_SIZE, LEVEL_GEN_EARTH_SIZE*2.5, True))
    else:
        last = game.gravitation_objects[-1]
        if screen.get_width() - last.position.x > 150:
            game.gravitation_objects.append(create_obstacle(screen))

