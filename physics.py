import logging
from math import sqrt
import pygame


def handle_boundary_collision(ball, center_pos_x, center_pos_y, boundary_radius):
    velocity_magnitude = sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)
    ball_pos_x, ball_pos_y = ball.pos_x, ball.pos_y

    distance_to_center = sqrt((center_pos_x - ball_pos_x) ** 2 + (center_pos_y - ball_pos_y) ** 2)

    logging.debug(
        f"Handling collision for ball at ({ball_pos_x}, {ball_pos_y}) with center at ({center_pos_x}, {center_pos_y})")

    if distance_to_center > (boundary_radius - ball.radius):
        if ball.sound:
            pygame.mixer.Sound.play(pygame.mixer.Sound(ball.sound))

        # logging.info(
        #     f"Collision detected at distance: {distance_to_center} with boundary at {boundary_radius - ball.radius}")

        while sqrt((center_pos_x - ball.pos_x) ** 2 + (center_pos_y - ball.pos_y) ** 2) > (
                boundary_radius - ball.radius):
            move_step = 0.2
            ball.pos_x += -ball.vel_x * move_step / velocity_magnitude
            ball.pos_y -= -ball.vel_y * move_step / velocity_magnitude

        normal_vector = (ball_pos_x - center_pos_x, ball_pos_y - center_pos_y)
        normal_magnitude = distance_to_center
        norm_x, norm_y = normal_vector[0] / normal_magnitude, normal_vector[1] / normal_magnitude

        velocity_direction = (ball.vel_x, -ball.vel_y)
        reflected_velocity = (
            velocity_direction[0] - 2 * (norm_x * velocity_direction[0] + norm_y * velocity_direction[1]) * norm_x,
            velocity_direction[1] - 2 * (norm_x * velocity_direction[0] + norm_y * velocity_direction[1]) * norm_y
        )

        ball.vel_x = reflected_velocity[0]
        ball.vel_y = -reflected_velocity[1]


def handle_ball_collision(self_ball, other_ball):
    dx = self_ball.pos_x - other_ball.pos_x
    dy = self_ball.pos_y - other_ball.pos_y
    distance = sqrt(dx ** 2 + dy ** 2)

    if distance < self_ball.radius + other_ball.radius:
        # Calculate normal and tangential velocities for this ball
        normal_x, normal_y = dx / distance, dy / distance
        tangent_x, tangent_y = -normal_y, normal_x

        # Decompose velocity components of both balls
        ball1_velocity_normal = normal_x * self_ball.vel_x + normal_y * self_ball.vel_y
        ball1_velocity_tangent = tangent_x * self_ball.vel_x + tangent_y * self_ball.vel_y
        other_ball_velocity_normal = normal_x * other_ball.vel_x + normal_y * other_ball.vel_y
        other_ball_velocity_tangent = tangent_x * other_ball.vel_x + tangent_y * other_ball.vel_y

        # Exchange normal velocity components (elastic collision)
        self_ball.vel_x = tangent_x * ball1_velocity_tangent + normal_x * other_ball_velocity_normal
        self_ball.vel_y = tangent_y * ball1_velocity_tangent + normal_y * other_ball_velocity_normal
        other_ball.vel_x = tangent_x * other_ball_velocity_tangent + normal_x * ball1_velocity_normal
        other_ball.vel_y = tangent_y * other_ball_velocity_tangent + normal_y * ball1_velocity_normal


def update_motion(ball):
    ball.vel_y += ball.acc
    ball.pos_x += ball.vel_x
    ball.pos_y -= ball.vel_y
    logging.debug(f"Ball motion updated: position ({ball.pos_x}, {ball.pos_y}), velocity ({ball.vel_x}, {ball.vel_y})")
