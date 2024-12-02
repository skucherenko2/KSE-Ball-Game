import math
from datetime import datetime
from random import randrange

import pygame
from pygame import Vector2

import Source.game as game
from Source.assets import AssetManager
from Source.config import PLAYER_ACCELERATION_SPEED, PLAYER_MAX_SPEED, PLAYER_MASS, GRAVITY_FORCE_MULTIPLIER, \
    PLAYER_SIZE, \
    TAKEOFF_FORCE, TAKEOFF_RANGE, LEVEL_BOUND_FRICTION_MULTIPLIER, PLAYER_FUEL_USE, TAKEOFF_FORCE_WITH_SIZE_SCALING, \
    ENGINE_RAND_POS
from Source.decorative_object import DecorativeSprite
from Source.level_utils import get_upper_bound, get_lower_bound
from Source.shake import add_shake
from Source.sound_channels import SoundChannel


class Player:
    def __init__(self):
        self.position = Vector2()
        self.velocity = Vector2()
        self.is_landed = False
        self.landed_position = None
        self.last_player_mirror_sound = datetime.now()
        self.ignores_gravity = None

    def get_look_angle(self) -> float:
        if self.is_landed:
            difference = self.landed_position - self.position
            return math.degrees(math.atan2(-difference.y, difference.x)) + 90
        else:
            return math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
    def move_towards_mouse(self):
        voice = pygame.mixer.Channel(SoundChannel.ENGINE.value)

        if game.death_time is not None:
            voice.stop()
            return

        if self.is_landed:
            voice.stop()
            if self.landed_position is None:
                return

            if pygame.mouse.get_pressed()[0] != 1 and pygame.key.get_pressed()[pygame.key.key_code("space")] != 1:
                return

            space_direction = self.position - self.landed_position
            space_direction = space_direction.normalize()

            self.position += space_direction * TAKEOFF_RANGE
            self.velocity.x += game.get_level_move_speed()
            self.add_to_velocity(space_direction, TAKEOFF_FORCE * self.landed_mass ** TAKEOFF_FORCE_WITH_SIZE_SCALING, True)
            self.is_landed = False
            self.landed_position = None
            self.ignores_gravity = datetime.now()
        else:
            if pygame.mouse.get_pressed()[0] != 1:
                voice.stop()
                return

            if game.fuel <= 0.1:
                voice.stop()
                return

            pos = Vector2(pygame.mouse.get_pos())
            towards_mouse = pos - self.position

            if towards_mouse.length() == 0:
                voice.stop()
                return

            towards_mouse = towards_mouse.normalize()

            distance = self.position.distance_to(pos)

            move_distance = min(distance, PLAYER_ACCELERATION_SPEED)

            self.add_to_velocity(towards_mouse, move_distance)

            if not voice.get_busy():
                voice.play(AssetManager.get_sound("engine.ogg"))

            smoke_surface = AssetManager.get_sprite("smoke").copy()
            smoke_surface = pygame.transform.rotate(smoke_surface, randrange(-180, 180))
            smoke_surface = pygame.transform.scale(smoke_surface, Vector2(PLAYER_SIZE, PLAYER_SIZE) * 2)

            new_smoke = DecorativeSprite(smoke_surface, self.position.copy() +
                                         Vector2(randrange(-ENGINE_RAND_POS, ENGINE_RAND_POS), randrange(-ENGINE_RAND_POS, ENGINE_RAND_POS))
                                         , 1, self.velocity)
            game.decorative_objects.append(new_smoke)

            game.use_fuel(PLAYER_FUEL_USE)

    def apply_gravitation(self):
        if self.is_landed:
            return

        if game.death_time is not None:
            return

        if self.ignores_gravity is not None:
            if (datetime.now() - self.ignores_gravity).total_seconds() > 0.1:
                self.ignores_gravity = None
            return

        self.velocity += self.calculate_gravitation()

    def calculate_gravitation(self, from_position=None) -> Vector2:
        velocity_plus = Vector2()
        player_position = from_position if from_position is not None else self.position
        for gravitation_object in game.gravitation_objects:
            direction = gravitation_object.position - player_position
            distance = direction.length() - gravitation_object.size
            direction = direction.normalize()

            force = (GRAVITY_FORCE_MULTIPLIER * (PLAYER_MASS * gravitation_object.mass)) / (distance ** 2)

            velocity_plus += direction * force

        return velocity_plus

    def add_to_velocity(self, direction: Vector2, power: float, ignore_limit = False):
        force = min(power, PLAYER_MAX_SPEED) if not ignore_limit else power
        self.velocity += direction * force

    def apply_velocity(self, dt, screen):
        if self.is_landed:
            return

        if game.death_time is not None:
            return

        self.position += self.velocity * dt

        if self.position.y > get_upper_bound(screen) - PLAYER_SIZE:
            self.position.y = get_upper_bound(screen) - PLAYER_SIZE
            self.velocity.y = -self.velocity.y * LEVEL_BOUND_FRICTION_MULTIPLIER
            self.play_mirror_sound_and_shake()
        elif self.position.y < get_lower_bound() + PLAYER_SIZE:
            self.position.y = get_lower_bound() + PLAYER_SIZE
            self.velocity.y = -self.velocity.y * LEVEL_BOUND_FRICTION_MULTIPLIER
            self.play_mirror_sound_and_shake()
        if self.position.x >= screen.get_width() - PLAYER_SIZE:
            self.position.x = screen.get_width() - PLAYER_SIZE
            self.velocity.x = -self.velocity.x * LEVEL_BOUND_FRICTION_MULTIPLIER
            self.play_mirror_sound_and_shake()

    def check_game_end(self):
        if self.position.x <= PLAYER_SIZE:
            if game.death_time is None:
                voice = pygame.mixer.Channel(SoundChannel.DEATH_EXPLOSION.value)
                voice.play(AssetManager.get_sound("explosion"))

                add_shake(0.2, 5)
                add_shake(1.2, 3)

                stop_voices = [SoundChannel.LAND, SoundChannel.WALL_MIRROR, SoundChannel.ENGINE, SoundChannel.FUEL_ALARM]
                for v in stop_voices:
                    pygame.mixer.Channel(v.value).stop()
                pygame.mixer.music.stop()

                game.death_time = datetime.now()

    def play_mirror_sound_and_shake(self):
        add_shake(0.2, 1)

        if (datetime.now() - self.last_player_mirror_sound).total_seconds() > 0.2:
            voice = pygame.mixer.Channel(SoundChannel.WALL_MIRROR.value)

            voice.play(AssetManager.get_sound("mirror"))
            self.last_player_mirror_sound = datetime.now()

    def draw_maneuvering_hints(self, screen):
        if self.is_landed:
            return

        future_position = self.position.copy()
        future_velocity = self.velocity.copy()
        last_pos = future_position.copy()

        for future_point in range(0, 15):
            future_position += (future_velocity * 0.016) / 0.07
            future_velocity += self.calculate_gravitation(future_position)

            pygame.draw.circle(screen, (0, 255, 0), future_position, int(PLAYER_SIZE / 2))
            pygame.draw.line(screen, (0, 255, 0), last_pos, future_position, int(PLAYER_SIZE / 2))

            for gravitation_object in game.gravitation_objects:
                if gravitation_object.position.distance_to(future_position) < PLAYER_SIZE + gravitation_object.size:
                    pygame.draw.circle(screen, (255, 0, 0), future_position, int(PLAYER_SIZE / 2))
                    pygame.draw.line(screen, (255, 0, 0), last_pos, future_position, int(PLAYER_SIZE / 2))
                    return

            last_pos = future_position.copy()

    last_player_mirror_sound = None
    position:Vector2
    velocity:Vector2
    is_landed:bool
    landed_position:Vector2 | None
    landed_mass:float