import logging
import pygame
from events import handle_events
from game_objects import BigCircle, BallPool
from graphics import setup_screen, load_background, draw_background, draw_big_circle, draw_balls, update_display
from constants import *
from physics import handle_boundary_collision, handle_ball_collision, update_motion

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

    def create_initial_balls(self):
        collision_sound = "audio/golf_ball.wav"
        logging.debug("Creating initial balls.")
        ball_radius = 10

        red_ball = self.ball_pool.acquire("Red Ball", RED, ball_radius, 5, -5,
                                          self.circleCentre[0] - self.circleCentre[1] + ball_radius,
                                          self.big_circle_radius, collision_sound)
        self.ball_pool.active_balls.append(red_ball)
        logging.info("Red ball acquired from pool and initialized.")

        gold_ball = self.ball_pool.acquire("GOLDEN Ball", GOLDEN, ball_radius, -5, 5,
                                           self.circleCentre[0] + self.circleCentre[1] - ball_radius,
                                           self.big_circle_radius, collision_sound)
        self.ball_pool.active_balls.append(gold_ball)
        logging.info("GOLDEN ball acquired from pool and initialized.")

    def wait_for_simulation_start(self):
        while not self.start_sim:
            self.screen.fill(DEEP_BLUE)
            draw_background(self.screen, self.background)
            self.start_sim = handle_events(pygame.event.get(), 'start_sim')
            pygame.display.update()
            logging.debug("Waiting for simulation start.")

    def run_simulation(self):
        self.create_initial_balls()

        while True:
            self.screen.fill(DEEP_BLUE)
            draw_big_circle(self.screen, self.big_circle)
            logging.debug("Main simulation loop running.")

            events = pygame.event.get()
            self.pause, self.trail = handle_events(events, 'runtime',
                                                   additional_params={'pause': self.pause, 'trail': self.trail})

            if not self.pause:
                self.update_balls()

            draw_balls(self.screen, self.ball_pool)
            update_display(self.clock, FPS)
            self.frames += 1

    def update_balls(self):
        for i, ball in enumerate(self.ball_pool.active_balls):
            handle_boundary_collision(ball, self.circleCentre[0], self.circleCentre[1], self.big_circle_radius)
            for other in self.ball_pool.active_balls[i + 1:]:
                handle_ball_collision(ball, other)
            update_motion(ball)
            ball.update_track(self.frames, self.trail, FPS)


if __name__ == "__main__":
    try:
        game = Game()
        game.wait_for_simulation_start()
        game.run_simulation()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        pygame.quit()
