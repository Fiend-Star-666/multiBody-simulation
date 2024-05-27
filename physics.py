import pygame
from math import sqrt
from game_objects import Ball, BigCircle


def update_ball_position():
    for ball in Ball.balls:
        ball.vel_y += ball.acc
        ball.pos_x += ball.vel_x
        ball.pos_y -= ball.vel_y


def handle_collisions():
    for ball in Ball.balls:
        vel = sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)
        x, y = BigCircle.center_x, BigCircle.center_y  # center of circle
        center_to_ball = sqrt((x - ball.pos_x) ** 2 + (y - ball.pos_y) ** 2)

        if center_to_ball >= (BigCircle.radius - ball.radius):
            pygame.mixer.Sound.play(pygame.mixer.Sound(ball.sound))

            # Collision response calculations...
            normal_x = ball.pos_x - x
            normal_y = ball.pos_y - y
            normal_mag = center_to_ball
            normal_x /= normal_mag
            normal_y /= normal_mag

            vel_x = ball.vel_x
            vel_y = -ball.vel_y
            dot_product = normal_x * vel_x + normal_y * vel_y

            reflected_x = vel_x - 2 * dot_product * normal_x
            reflected_y = vel_y - 2 * dot_product * normal_y

            ball.vel_x = reflected_x
            ball.vel_y = -reflected_y
