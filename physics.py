import logging
from math import sqrt

import pygame

'''
def handle_boundary_collision(ball, center_pos_x, center_pos_y, boundary_radius):
    velocity_squared = ball.vel_x ** 2 + ball.vel_y ** 2
    ball_pos_x, ball_pos_y = ball.pos_x, ball.pos_y

    dx = center_pos_x - ball_pos_x
    dy = center_pos_y - ball_pos_y
    distance_squared_to_center = dx ** 2 + dy ** 2
    boundary_limit_squared = (boundary_radius - ball.radius) ** 2

    logging.debug(
        f"Handling boundary collision: ball at ({ball_pos_x}, {ball_pos_y}), center at ({center_pos_x}, {center_pos_y}), distance squared to center: {distance_squared_to_center}, boundary limit squared: {boundary_limit_squared}")

    if distance_squared_to_center > boundary_limit_squared:
        if ball.sound:
            pygame.mixer.Sound.play(pygame.mixer.Sound(ball.sound))
            logging.info("Collision sound played")

        move_step = 0.2
        move_scale = move_step / sqrt(velocity_squared)

        while distance_squared_to_center > boundary_limit_squared:
            ball_pos_x -= ball.vel_x * move_scale
            ball_pos_y -= ball.vel_y * move_scale
            dx = center_pos_x - ball_pos_x
            dy = center_pos_y - ball_pos_y
            distance_squared_to_center = dx ** 2 + dy ** 2

        distance_to_center = sqrt(distance_squared_to_center)
        norm_x, norm_y = dx / distance_to_center, dy / distance_to_center

        vel_x, vel_y = ball.vel_x, ball.vel_y
        dot_product = norm_x * vel_x + norm_y * vel_y

        reflected_velocity_x = vel_x - 2 * dot_product * norm_x
        reflected_velocity_y = vel_y - 2 * dot_product * norm_y

        ball.vel_x = reflected_velocity_x
        ball.vel_y = reflected_velocity_y
        ball.pos_x = ball_pos_x
        ball.pos_y = ball_pos_y

        logging.debug(
            f"Boundary collision resolved: new position ({ball.pos_x}, {ball.pos_y}), new velocity ({ball.vel_x}, {ball.vel_y})")


def handle_ball_collision(self_ball, other_ball):
    dx = self_ball.pos_x - other_ball.pos_x
    dy = self_ball.pos_y - other_ball.pos_y
    distance_squared = dx ** 2 + dy ** 2
    radius_sum = self_ball.radius + other_ball.radius
    radius_sum_squared = radius_sum ** 2

    logging.debug(
        f"Handling ball collision: self_ball at ({self_ball.pos_x}, {self_ball.pos_y}), other_ball at ({other_ball.pos_x}, {other_ball.pos_y}), distance squared: {distance_squared}, radius sum squared: {radius_sum_squared}")

    if distance_squared < radius_sum_squared:
        distance = sqrt(distance_squared)
        overlap = radius_sum - distance

        # Normalize the vector between the balls
        normal_x, normal_y = dx / distance, dy / distance

        # Separate the balls based on their masses (assuming equal masses here)
        self_ball.pos_x += normal_x * (overlap / 2)
        self_ball.pos_y += normal_y * (overlap / 2)
        other_ball.pos_x -= normal_x * (overlap / 2)
        other_ball.pos_y -= normal_y * (overlap / 2)

        logging.debug(
            f"Balls separated: self_ball at ({self_ball.pos_x}, {self_ball.pos_y}), other_ball at ({other_ball.pos_x}, {other_ball.pos_y})")

        # Calculate normal and tangential velocities for this ball
        tangent_x, tangent_y = -normal_y, normal_x

        self_ball_vel_x, self_ball_vel_y = self_ball.vel_x, self_ball.vel_y
        other_ball_vel_x, other_ball_vel_y = other_ball.vel_x, other_ball.vel_y

        # Decompose velocity components of both balls
        ball1_velocity_normal = normal_x * self_ball_vel_x + normal_y * self_ball_vel_y
        ball1_velocity_tangent = tangent_x * self_ball_vel_x + tangent_y * self_ball_vel_y
        other_ball_velocity_normal = normal_x * other_ball_vel_x + normal_y * other_ball_vel_y
        other_ball_velocity_tangent = tangent_x * other_ball_vel_x + tangent_y * other_ball_vel_y

        # Exchange normal velocity components (elastic collision)
        self_ball.vel_x = tangent_x * ball1_velocity_tangent + normal_x * other_ball_velocity_normal
        self_ball.vel_y = tangent_y * ball1_velocity_tangent + normal_y * other_ball_velocity_normal
        other_ball.vel_x = tangent_x * other_ball_velocity_tangent + normal_x * ball1_velocity_normal
        other_ball.vel_y = tangent_y * other_ball_velocity_tangent + normal_y * ball1_velocity_normal

        logging.debug(
            f"Ball collision resolved: self_ball velocity ({self_ball.vel_x}, {self_ball.vel_y}), other_ball velocity ({other_ball.vel_x}, {other_ball.vel_y})")
'''


def update_motion(ball):
    ball.vel_y += ball.acc
    ball.pos_x += ball.vel_x
    ball.pos_y -= ball.vel_y
    logging.debug(f"Ball motion updated: position ({ball.pos_x}, {ball.pos_y}), velocity ({ball.vel_x}, {ball.vel_y})")


def handle_boundary_collision(ball, center_pos_x, center_pos_y, boundary_radius):
    velocity_magnitude = sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)
    ball_pos_x, ball_pos_y = ball.pos_x, ball.pos_y

    dx = center_pos_x - ball_pos_x
    dy = center_pos_y - ball_pos_y
    distance_to_center = sqrt(dx ** 2 + dy ** 2)
    boundary_limit = boundary_radius - ball.radius

    # logging.debug(
    #     f"Handling collision for ball at ({ball_pos_x}, {ball_pos_y}) with center at ({center_pos_x}, {center_pos_y})"
    # )

    if distance_to_center > boundary_limit:
        if ball.sound:
            pygame.mixer.Sound.play(pygame.mixer.Sound(ball.sound))

        # logging.info(
        #     f"Collision detected at distance: {distance_to_center} with boundary at {boundary_limit}"
        # )

        move_step = 0.2
        move_scale = move_step / velocity_magnitude

        while distance_to_center > boundary_limit:
            ball_pos_x += -ball.vel_x * move_scale
            ball_pos_y -= -ball.vel_y * move_scale
            dx = center_pos_x - ball_pos_x
            dy = center_pos_y - ball_pos_y
            distance_to_center = sqrt(dx ** 2 + dy ** 2)

        norm_x, norm_y = dx / distance_to_center, dy / distance_to_center

        vel_x, vel_y = ball.vel_x, -ball.vel_y
        dot_product = norm_x * vel_x + norm_y * vel_y

        reflected_velocity_x = vel_x - 2 * dot_product * norm_x
        reflected_velocity_y = vel_y - 2 * dot_product * norm_y

        ball.vel_x = reflected_velocity_x
        ball.vel_y = -reflected_velocity_y
        ball.pos_x = ball_pos_x
        ball.pos_y = ball_pos_y


def handle_ball_collision(self_ball, other_ball):
    dx = self_ball.pos_x - other_ball.pos_x
    dy = self_ball.pos_y - other_ball.pos_y
    distance = sqrt(dx ** 2 + dy ** 2)

    if distance < self_ball.radius + other_ball.radius:
        # Calculate normal and tangential velocities for this ball
        normal_x, normal_y = dx / distance, dy / distance
        tangent_x, tangent_y = -normal_y, normal_x

        self_ball_vel_x, self_ball_vel_y = self_ball.vel_x, self_ball.vel_y
        other_ball_vel_x, other_ball_vel_y = other_ball.vel_x, other_ball.vel_y

        # Decompose velocity components of both balls
        ball1_velocity_normal = normal_x * self_ball_vel_x + normal_y * self_ball_vel_y
        ball1_velocity_tangent = tangent_x * self_ball_vel_x + tangent_y * self_ball_vel_y
        other_ball_velocity_normal = normal_x * other_ball_vel_x + normal_y * other_ball_vel_y
        other_ball_velocity_tangent = tangent_x * other_ball_vel_x + tangent_y * other_ball_vel_y

        # Exchange normal velocity components (elastic collision)
        self_ball.vel_x = tangent_x * ball1_velocity_tangent + normal_x * other_ball_velocity_normal
        self_ball.vel_y = tangent_y * ball1_velocity_tangent + normal_y * other_ball_velocity_normal
        other_ball.vel_x = tangent_x * other_ball_velocity_tangent + normal_x * ball1_velocity_normal
        other_ball.vel_y = tangent_y * other_ball_velocity_tangent + normal_y * ball1_velocity_normal

def handle_ball_collision_new(self_ball, other_ball):
    logging.debug(f"Handling collision between self_ball at ({self_ball.pos_x}, {self_ball.pos_y}) "
                  f"and other_ball at ({other_ball.pos_x}, {other_ball.pos_y})")

    dx = self_ball.pos_x - other_ball.pos_x
    dy = self_ball.pos_y = other_ball.pos_y
    distance = sqrt(dx ** 2 + dy ** 2)

    logging.debug(f"dx: {dx}, dy: {dy}, distance: {distance}")

    if distance < self_ball.radius + other_ball.radius:
        logging.debug("Collision detected")
        # Calculate normal and tangential velocities for this ball
        normal_x, normal_y = dx / distance, dy / distance
        tangent_x, tangent_y = -normal_y, normal_x

        logging.debug(f"Normal vector: ({normal_x}, {normal_y}), Tangent vector: ({tangent_x}, {tangent_y})")

        self_ball_vel_x, self_ball_vel_y = self_ball.vel_x, self_ball.vel_y
        other_ball_vel_x, other_ball_vel_y = other_ball.vel_x, other_ball.vel_y

        # Decompose velocity components of both balls
        ball1_velocity_normal = normal_x * self_ball_vel_x + normal_y * self_ball_vel_y
        ball1_velocity_tangent = tangent_x * self_ball_vel_x + tangent_y * self_ball_vel_y
        other_ball_velocity_normal = normal_x * other_ball_vel_x + normal_y * other_ball_vel_y
        other_ball_velocity_tangent = tangent_x * other_ball_vel_x + tangent_y * other_ball_vel_y

        logging.debug(f"Ball1 normal velocity: {ball1_velocity_normal}, tangent velocity: {ball1_velocity_tangent}")
        logging.debug(f"Other ball normal velocity: {other_ball_velocity_normal}, tangent velocity: {other_ball_velocity_tangent}")

        # Exchange normal velocity components (elastic collision)
        self_ball.vel_x = tangent_x * ball1_velocity_tangent + normal_x * other_ball_velocity_normal
        self_ball.vel_y = tangent_y * ball1_velocity_tangent + normal_y * other_ball_velocity_normal
        other_ball.vel_x = tangent_x * other_ball_velocity_tangent + normal_x * ball1_velocity_normal
        other_ball.vel_y = tangent_y * other_ball_velocity_tangent + normal_y * ball1_velocity_normal

        logging.debug(f"Updated self_ball velocity: ({self_ball.vel_x}, {self_ball.vel_y})")
        logging.debug(f"Updated other_ball velocity: ({other_ball.vel_x}, {other_ball.vel_y})")

        # Handle ball overlap by adjusting positions
        overlap = 0.5 * (self_ball.radius + other_ball.radius - distance)
        logging.debug(f"Overlap: {overlap}")

        self_ball.pos_x += overlap * normal_x
        self_ball.pos_y += overlap * normal_y
        other_ball.pos_x -= overlap * normal_x
        other_ball.pos_y -= overlap * normal_y

        logging.debug(f"Updated self_ball position: ({self_ball.pos_x}, {self_ball.pos_y})")
        logging.debug(f"Updated other_ball position: ({other_ball.pos_x}, {other_ball.pos_y})")
    else:
        logging.debug("No collision detected")