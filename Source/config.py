import pygame

PLAYER_ACCELERATION_SPEED = 5
PLAYER_MAX_SPEED = 50
PLAYER_MASS = 1
PLAYER_SIZE = 10
PLAYER_FUEL_USE = 0.1
PLAYER_FUEL_REGEN = 0.05
PLAYER_FUEL_MAX = 100

ENGINE_RAND_POS = 8

TAKEOFF_FORCE = 25
TAKEOFF_FORCE_WITH_SIZE_SCALING = 0.7
TAKEOFF_RANGE = PLAYER_SIZE * 1

GRAVITY_FORCE_MULTIPLIER = 1000

LEVEL_BOUND_PX_SIZE = 70
LEVEL_BOUND_FRICTION_MULTIPLIER = 0.7

LEVEL_GEN_EARTH_SIZE = 20

pygame.font.init()
default_font = pygame.font.SysFont('Comic Sans MS', 30)
warning_font = pygame.font.SysFont('Comic Sans MS', 160)