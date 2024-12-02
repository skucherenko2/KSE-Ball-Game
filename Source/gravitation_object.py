
import pygame
from pygame import Vector2, Surface, Color

import Source.game as game
from Source.assets import AssetManager
from Source.config import PLAYER_SIZE
from Source.decorative_object import DecorativeText
from Source.player import Player
from Source.sound_channels import SoundChannel


class GravitationObject:
    def __init__(self, position: Vector2, mass: float, size: float, initial: bool = False):
        self.position = position
        self.mass = mass
        self.size = size
        self.surface = AssetManager.get_random_planet_sprite() if not initial else AssetManager.get_sprite("earth")
        self.surface = pygame.transform.scale(self.surface, (size*2, size*2))

    def render(self, screen):
        #pygame.draw.circle(screen, (0, 255, 0), self.position, self.size)
        screen.blit(self.surface, self.position - Vector2(self.size, self.size))

    @staticmethod
    def try_placing_decorative(player:Player):
        all_distances = list((x.position.distance_to(player.position) for x in game.decorative_objects if type(x) == DecorativeText))
        if len(all_distances) != 0:
            min_distance = min(all_distances)
            if min_distance < 50:
                return
            GravitationObject.place_landing_decorative(player)
        else:
            GravitationObject.place_landing_decorative(player)

    @staticmethod
    def place_landing_decorative(player:Player):
        game.decorative_objects.append(
            DecorativeText(
                "Landed", Color("green"), 1.5, player.position
            )
        )

    def try_landing(self, player:Player):
        if game.death_time is not None:
            return

        distance = game.player.position.distance_to(self.position)
        direction = game.player.position - self.position
        direction = direction.normalize()

        if distance < self.size + PLAYER_SIZE:
            if not player.is_landed:
                self.try_placing_decorative(player)

                voice = pygame.mixer.Channel(SoundChannel.LAND.value)
                voice.set_volume(0.35)

                if not voice.get_busy():
                    voice.play(AssetManager.get_sound("land"), fade_ms=800)

                player.is_landed = True
                player.position = self.position + direction * (self.size + PLAYER_SIZE - 1)
                player.landed_position = self.position
                player.velocity = Vector2()
                player.landed_mass = self.mass

    position:Vector2
    mass:float
    surface:Surface