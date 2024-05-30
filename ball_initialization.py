import logging
from constants import *


def create_initial_balls(ball_pool, circle_centre, big_circle_radius):
    collision_sound = "audio/golf_ball.wav"
    logging.debug("Creating initial balls.")
    ball_radius = 8

    balls_info = [
        ("Red Ball", RED, 5, -5, circle_centre[0] - circle_centre[1] + ball_radius),
        ("GOLDEN Ball", GOLDEN, -5, 4, circle_centre[0] + circle_centre[1] - ball_radius),
        # ("Green Ball", GREEN, 4.25, -4.5, circle_centre[0] - circle_centre[1] + 2 * ball_radius),
        # ("Blue Ball", BLUE, -4, 4, circle_centre[0] + circle_centre[1] - 2 * ball_radius),
        # ("Magenta Ball", MAGENTA, -3, +6, circle_centre[0] - circle_centre[1] + 3 * ball_radius),
        # ("Yellow Ball", TASTY_YELLOW, -3, 3, circle_centre[0] + circle_centre[1] - 3 * ball_radius)
    ]

    for ball_name, color, vx, vy, initial_x in balls_info:
        ball = ball_pool.acquire(ball_name, color, ball_radius, vx, vy,
                                 initial_x, big_circle_radius, collision_sound)
        if ball is not None:
            ball_pool.active_balls.append(ball)
            logging.info(f"{ball_name} acquired from pool and initialized.")
        else:
            logging.warning(f"Failed to acquire {ball_name} from pool.")
