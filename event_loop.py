import pygame
import logging
from events import handle_events
from graphics import draw_background, draw_big_circle, draw_balls, update_display
from constants import DEEP_BLUE, FPS


def wait_for_simulation_start(screen, background):
    start_sim = False
    while not start_sim:
        screen.fill(DEEP_BLUE)
        draw_background(screen, background)
        start_sim = handle_events(pygame.event.get(), 'start_sim')
        pygame.display.update()
        logging.debug("Waiting for simulation start.")


def run_simulation(game):
    while True:
        game.screen.fill(DEEP_BLUE)
        draw_big_circle(game.screen, game.big_circle)
        logging.debug("Main simulation loop running.")

        events = pygame.event.get()
        game.pause, game.trail = handle_events(events, 'runtime',
                                               additional_params={'pause': game.pause, 'trail': game.trail})

        if not game.pause:
            game.update_balls()

        draw_balls(game.screen, game.ball_pool)
        update_display(game.clock, FPS)
        game.frames += 1
