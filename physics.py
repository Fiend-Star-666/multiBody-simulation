import logging
from math import sqrt

import pygame


def handle_boundary_collision(self, center_pos_x, center_pos_y, boundary_radius):
    velocity_magnitude = sqrt(self.vel_x ** 2 + self.vel_y ** 2)
    ball_pos_x, ball_pos_y = self.pos_x, self.pos_y
    vel_x, vel_y = self.vel_x, self.vel_y

    distance_to_center = sqrt((center_pos_x - ball_pos_x) ** 2 + (center_pos_y - ball_pos_y) ** 2)

    logging.debug(
        f"Handling collision for ball at ({ball_pos_x}, {ball_pos_y}) with center at ({center_pos_x}, {center_pos_y})")

    if distance_to_center > (boundary_radius - self.radius):

        if self.sound:
            pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))

        logging.info(
            f"Collision detected at distance: {distance_to_center} with boundary at {boundary_radius - self.radius}")

        while sqrt((center_pos_x - self.pos_x) ** 2 + (center_pos_y - self.pos_y) ** 2) > (
                boundary_radius - self.radius):
            move_step = 0.2
            self.pos_x += -self.vel_x * move_step / velocity_magnitude
            self.pos_y -= -self.vel_y * move_step / velocity_magnitude

        normal_vector = (ball_pos_x - center_pos_x, ball_pos_y - center_pos_y)
        normal_magnitude = distance_to_center
        norm_x, norm_y = normal_vector[0] / normal_magnitude, normal_vector[1] / normal_magnitude

        velocity_direction = (vel_x, -vel_y)
        reflected_velocity = (
            velocity_direction[0] - 2 * (norm_x * velocity_direction[0] + norm_y * velocity_direction[1]) * norm_x,
            velocity_direction[1] - 2 * (norm_x * velocity_direction[0] + norm_y * velocity_direction[1]) * norm_y
        )

        self.vel_x = reflected_velocity[0]
        self.vel_y = -reflected_velocity[1]


def handle_ball_collision(self, other):
    dx = self.pos_x - other.pos_x
    dy = self.pos_y - other.pos_y
    distance = sqrt(dx ** 2 + dy ** 2)

    if distance < self.radius + other.radius:
        # Calculate normal and tangential velocities for this ball
        nx, ny = dx / distance, dy / distance
        tx, ty = -ny, nx

        # Decompose velocity components of both balls
        v1n = nx * self.vel_x + ny * self.vel_y
        v1t = tx * self.vel_x + ty * self.vel_y
        v2n = nx * other.vel_x + ny * other.vel_y
        v2t = tx * other.vel_x + ty * other.vel_y

        # Exchange normal velocity components (elastic collision)
        self.vel_x = tx * v1t + nx * v2n
        self.vel_y = ty * v1t + ny * v2n
        other.vel_x = tx * v2t + nx * v1n
        other.vel_y = ty * v2t + ny * v1n


def update_motion(self):
    self.vel_y += self.acc
    self.pos_x += self.vel_x
    self.pos_y -= self.vel_y
    logging.debug(
        f"Ball motion updated: position ({self.pos_x}, {self.pos_y}), velocity ({self.vel_x}, {self.vel_y})")

