import logging

import pygame

from ball_initialization import create_initial_balls
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, WINDOW_POSITION, BLUISH_WHITE, CIRCLE_WIDTH, CIRCLE_HEIGHT, FPS
from event_loop import wait_for_simulation_start, run_simulation
from game_objects import BigCircle, BallPool
from graphics import setup_screen, load_background
from logging_setup import setup_logging
from physics import handle_boundary_collision, handle_ball_collision, update_motion


class Game:
    def __init__(self):
        pygame.init()
        self.screen = setup_screen(DISPLAY_WIDTH, DISPLAY_HEIGHT, WINDOW_POSITION)
        pygame.display.set_caption("Bouncing Balls")
        self.clock = pygame.time.Clock()
        self.background = load_background("img/start_img.png")
        self.circleCentre = (CIRCLE_WIDTH // 2, CIRCLE_HEIGHT // 2)
        self.big_circle_radius = CIRCLE_HEIGHT // 2
        self.big_circle = BigCircle(self.circleCentre[0], self.circleCentre[1], self.big_circle_radius, BLUISH_WHITE)
        self.pause = False
        self.start_sim = False
        self.trail = True
        self.frames = 0
        self.ball_pool = BallPool(10)
        logging.debug("Game initialized with main window and big circle setup.")

    def update_balls(self):
        for i, ball in enumerate(self.ball_pool.active_balls):
            handle_boundary_collision(ball, self.circleCentre[0], self.circleCentre[1], self.big_circle_radius)
            for other in self.ball_pool.active_balls[i + 1:]:
                handle_ball_collision(ball, other)
            update_motion(ball)
            ball.update_motion_trace(self.frames, self.trail, FPS)


if __name__ == "__main__":
    setup_logging()
    try:
        game = Game()
        wait_for_simulation_start(game.screen, game.background)
        create_initial_balls(game.ball_pool, game.circleCentre, game.big_circle_radius)
        run_simulation(game)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        pygame.quit()
