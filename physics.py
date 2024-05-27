import pygame
from math import sqrt
from game_objects import Ball, BigCircle


def update_ball_position():
    for ball in Ball.balls:
        # Assuming positive acceleration downwards
        ball.vel_y -= ball.acc
        ball.pos_x += ball.vel_x
        ball.pos_y += ball.vel_y  # Positive y should increase downward if gravity is downwards


def handle_collisions(big_circle):
    for ball in Ball.balls:
        # Retrieve the center coordinates of the big circle
        circle_center_x, circle_center_y = big_circle.center_x, big_circle.center_y

        # Calculate the distance from the center of the big circle to the ball
        distance_to_ball = sqrt((circle_center_x - ball.pos_x) ** 2 + (circle_center_y - ball.pos_y) ** 2)

        # Check if the ball is colliding with or inside the big circle
        if distance_to_ball <= (big_circle.radius + ball.radius):
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
            ball.vel_y = reflected_velocity_y  # Reflection based on the collision normal

            # Optionally, add damping to simulate energy loss
            damping_factor = 0.9  # Less than 1 to reduce velocity
            ball.vel_x *= damping_factor
            ball.vel_y *= damping_factor

