from enum import Enum

import pygame
from pygame import QUIT, Vector2

from Source import game
from Source.assets import AssetManager
from Source.config import PLAYER_SIZE
from Source.decorative_object import DecorativeText, DecorativeSprite
from Source.level_utils import draw_bounds, draw_death_wall
from Source.obstacle_generator import try_generating_new_obstacle
from Source.shake import get_shake_summ
from Source.ui import draw_main_ui, draw_menu_ui, draw_death_ui

game.master_init()

clock = pygame.time.Clock()
fps = 60
dt = 0
fpsClock = pygame.time.Clock()

running = True
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('KSE Ball Game')

game_paused = False

def reset_game():
    game.reset_game(screen)
    global game_paused

    game_paused = False
    pygame.mixer.music.unpause()
    pygame.mixer.unpause()
    pygame.mixer.music.load(AssetManager.get_music_path("ambience"))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

def update_menu_screen():
    draw_menu_ui(screen)

def update_game_screen():
    # Update.

    if not game_paused:
        # Player
        game.player.check_game_end()

        game.player.move_towards_mouse()
        game.player.apply_gravitation()
        game.player.apply_velocity(dt, screen)

        # Physics
        game.tick_physics(dt)
        try_generating_new_obstacle(screen)

    # Draw

    # Draw objects
    for gravitation_object in game.gravitation_objects:
        gravitation_object.render(screen)
        gravitation_object.try_landing(game.player)

        # Draw smoke
    for decorative_object in game.decorative_objects:
        if type(decorative_object) == DecorativeSprite:
            decorative_object.render(screen, dt)

        # Draw player
    game.player.draw_maneuvering_hints(screen)

    player_surface = AssetManager.get_sprite("player")
    player_surface = pygame.transform.scale(player_surface, Vector2(PLAYER_SIZE, PLAYER_SIZE) * 4)
    player_surface = pygame.transform.rotate(player_surface, game.player.get_look_angle())

    screen.blit(player_surface, game.player.position - Vector2(player_surface.get_size()) / 2)
    # Draw level
    draw_death_wall(screen)
    draw_bounds(screen)

    # Draw decorative text
    for decorative_object in game.decorative_objects:
        if type(decorative_object) == DecorativeText:
            decorative_object.render(screen, dt)

        # Draw UI
    draw_main_ui(screen, game_paused)

    if game.death_time is not None:
        if not game.game_finished:
            game.try_finish_game()
        else:
            draw_death_ui(screen)

class GameScreen(Enum):
    Menu=0
    Game=1
game_screen = GameScreen.Menu

# Game loop.
while running:
    background = AssetManager.get_sprite("background.jpg")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),
                                             pygame.RESIZABLE)
        if game_screen == GameScreen.Game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused

                    if game_paused:
                        pygame.mixer.pause()
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.unpause()
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_TAB and game.game_finished:
                    game_screen = GameScreen.Menu
        elif game_screen == GameScreen.Menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    reset_game()
                    game_screen = GameScreen.Game

    match game_screen:
        case GameScreen.Menu:
            update_menu_screen()
        case GameScreen.Game:
            update_game_screen()

        # Apply shake
    final_surface = screen.copy()
    screen.fill("black")
    screen.blit(final_surface, get_shake_summ())

    pygame.display.flip()
    fpsClock.tick(fps)
    dt = clock.tick(60) / 1000

pygame.quit()