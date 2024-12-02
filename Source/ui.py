from datetime import datetime
from math import sin

import pygame
from pygame import Color, Vector2, Surface
from pygame.math import lerp

from Source import game
from Source.assets import AssetManager
from Source.config import default_font, warning_font, PLAYER_FUEL_MAX
from Source.score import get_highscore
from Source.sound_channels import SoundChannel

game_start_time = datetime.now()

def draw_menu_ui(screen: Surface):
    title_text = warning_font.render("KSE ball game", False, (255, 255, 255))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 0.7) / 2 - Vector2(title_text.get_size()) / 2)
    title_text = default_font.render("press TAB to start", False, (255, 255, 255))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 1.3) / 2 - Vector2(title_text.get_size()) / 2)
    if get_highscore() is not None:
        title_text = default_font.render(f"Highscore is: {get_highscore()}", False, (255, 255, 255))
        screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 1.7) / 2 - Vector2(title_text.get_size()) / 2)

def draw_main_ui(screen, game_paused):
    fuel_percentage = game.fuel / PLAYER_FUEL_MAX
    fuel_color = Color(int(lerp(255, 0, fuel_percentage)), int(lerp(0, 255, fuel_percentage)), 0)
    fuel_text = default_font.render(f"Fuel: {int(game.fuel)}", False, fuel_color)
    screen.blit(fuel_text, (10, 10))

    score_text = default_font.render(f"Score: {game.score}", False, (0, 255, 0))
    screen.blit(score_text, (50 + fuel_text.get_width(), 10))

    if get_highscore() is not None:
        score_text = default_font.render(f"Highscore: {get_highscore()}", False, (0, 255, 0))
        screen.blit(score_text, (50 + score_text.get_width() + fuel_text.get_width(), 10))

    if game_paused:
        paused_text = warning_font.render("GAME PAUSED", False, Color("yellow"))
        screen.blit(paused_text, Vector2(screen.get_rect().center) - Vector2(paused_text.get_size()) / 2)
    else:
        voice = pygame.mixer.Channel(SoundChannel.FUEL_ALARM.value)
        if fuel_percentage < 0.1 and game.death_time is None:
            if not voice.get_busy():
                voice.play(AssetManager.get_sound("alarm"))
            fuel_warning = warning_font.render("FUEL LOW", False, Color("red"))
            delta = datetime.now() - game_start_time
            fuel_warning.set_alpha(abs(sin(delta.total_seconds() * 3)) * 255)
            screen.blit(fuel_warning, Vector2(screen.get_rect().center) - Vector2(fuel_warning.get_size()) / 2)
        else:
            voice.stop()

def draw_death_ui(screen):
    shadow = Surface((screen.get_width(), screen.get_height()))
    shadow.fill((0, 0, 0))
    shadow.set_alpha(100)
    screen.blit(shadow, (0, 0))

    new_highscore = False
    if game.score >= get_highscore():
        new_highscore = True

    title_text = warning_font.render("Game over", False, (255, 200, 200))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 0.6) / 2 - Vector2(title_text.get_size()) / 2)
    title_text = default_font.render(f"Score is: {game.score}", False, (255, 255, 255))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 1.2) / 2 - Vector2(title_text.get_size()) / 2)
    title_text = default_font.render(f"Highscore is: {get_highscore()}" + ("" if not new_highscore else " (new!)"), False, (255, 255, 255))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 1.4) / 2 - Vector2(title_text.get_size()) / 2)
    title_text = default_font.render("press TAB to return", False, (255, 255, 255))
    screen.blit(title_text, Vector2(screen.get_width(), screen.get_height() * 1.7) / 2 - Vector2(title_text.get_size()) / 2)

