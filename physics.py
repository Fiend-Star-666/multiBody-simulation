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
        # Calculate current velocity magnitude
        velocity_magnitude = sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)
        # Retrieve the center coordinates of the big circle
        circle_center_x, circle_center_y = BigCircle.center_x, BigCircle.center_y

        # Calculate the distance from the center of the big circle to the ball
        distance_to_ball = sqrt((circle_center_x - ball.pos_x) ** 2 + (circle_center_y - ball.pos_y) ** 2)

        # Check if the ball is colliding with the big circle
        if distance_to_ball >= (BigCircle.radius - ball.radius):
            # Play collision sound
            pygame.mixer.Sound.play(pygame.mixer.Sound(ball.sound))

            # Calculate the collision normal vector
            normal_x = ball.pos_x - circle_center_x
            normal_y = ball.pos_y - circle_center_y
            normal_magnitude = distance_to_ball
            normal_x /= normal_magnitude
            normal_y /= normal_magnitude

            # Calculate the incoming velocity vector
            incoming_velocity_x = ball.vel_x
            incoming_velocity_y = ball.vel_y

            # Calculate the dot product of the normal vector and the velocity vector
            dot_product = normal_x * incoming_velocity_x + normal_y * incoming_velocity_y

            # Calculate the reflected velocity components
            reflected_velocity_x = incoming_velocity_x - 2 * dot_product * normal_x
            reflected_velocity_y = incoming_velocity_y - 2 * dot_product * normal_y

            # Update the ball's velocity with the reflected components
            ball.vel_x = reflected_velocity_x
            ball.vel_y = -reflected_velocity_y

