import os
from pathlib import Path
from random import randrange

import pygame
from pygame import Surface


def get_all_files_in_dir(start_path) -> dict:
    collected = {}
    initial_path = str(Path(os.getcwd())) + start_path
    for root, dirs, files in os.walk(initial_path):
        for file in files:
            collected[file] = os.path.join(root, file)

    return collected

class AssetManager:
    @staticmethod
    def collect_assets():
        sprites_sources = get_all_files_in_dir("\\Resources\\Sprites")
        for sprite_name, sprite_source in sprites_sources.items():
            AssetManager.sprite_surfaces_loaded[sprite_name] = pygame.image.load(sprite_source)
        sounds_sources = get_all_files_in_dir("\\Resources\\Sounds")
        for sound_name, sound_source in sounds_sources.items():
            AssetManager.sounds_loaded[sound_name] = pygame.mixer.Sound(sound_source)
        music_sources = get_all_files_in_dir("\\Resources\\Music")
        for music_name, music_source in music_sources.items():
            AssetManager.music_loaded[music_name] = music_source

    @staticmethod
    def get_sprite(sprite_id: str) -> Surface:
        if "." not in sprite_id:
            sprite_id = sprite_id + ".png"
        return AssetManager.sprite_surfaces_loaded[sprite_id]

    @staticmethod
    def get_sound(sound_id: str) -> pygame.mixer.Sound:
        if "." not in sound_id:
            sound_id = sound_id + ".wav"
        return AssetManager.sounds_loaded[sound_id]

    @staticmethod
    def get_music_path(music_id: str) -> str:
        if "." not in music_id:
            music_id = music_id + ".wav"
        return AssetManager.music_loaded[music_id]

    @staticmethod
    def get_random_planet_sprite() -> Surface:
        index = randrange(1, 6)
        return AssetManager.get_sprite(f"{index}.png")


    sprite_surfaces_loaded: dict[str, Surface] = {}
    sounds_loaded: dict[str, pygame.mixer.Sound] = {}
    music_loaded: dict[str, str] = {}
