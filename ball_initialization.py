import logging
from constants import RED, GOLDEN


def create_initial_balls(ball_pool, circle_centre, big_circle_radius):
    collision_sound = "audio/golf_ball.wav"
    logging.debug("Creating initial balls.")
    ball_radius = 10

    red_ball = ball_pool.acquire("Red Ball", RED, ball_radius, 5, -5,
                                 circle_centre[0] - circle_centre[1] + ball_radius,
                                 big_circle_radius, collision_sound)
    ball_pool.active_balls.append(red_ball)
    logging.info("Red ball acquired from pool and initialized.")

    gold_ball = ball_pool.acquire("GOLDEN Ball", GOLDEN, ball_radius, -5, 5,
                                  circle_centre[0] + circle_centre[1] - ball_radius,
                                  big_circle_radius, collision_sound)
    ball_pool.active_balls.append(gold_ball)
    logging.info("GOLDEN ball acquired from pool and initialized.")
