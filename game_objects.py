from math import sqrt, hypot
import logging
import pygame
import pygame.gfxdraw

from constants import *


class Ball:
    balls = []

    def __init__(self, name, color, radius, vel_x, vel_y, pos_x, pos_y, sound):
        self.name = name
        self.color = color
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sound = sound
        self.acc = GRAVITY  # Acceleration, can be set accordingly
        self.thickness = 0  # Border thickness for drawing
        self.track = []
        # Ball.balls.append(self)

    def reset(self, name, color, radius, vel_x, vel_y, pos_x, pos_y, sound="audio/golf_ball.wav"):
        self.name = name
        self.color = color
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sound = sound
        self.acc = 0
        self.track.clear()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius, self.thickness)

    # def handle_collision(self, center_x, center_y, big_radius):
    #     velocity_magnitude = sqrt(self.vel_x ** 2 + self.vel_y ** 2)
    #     ball_x, ball_y = self.pos_x, self.pos_y
    #
    #     # Calculate the distance from the ball to the circle's center
    #     distance_to_center = sqrt((center_x - ball_x) ** 2 + (center_y - ball_y) ** 2)
    #     logging.debug(f"Handling collision for ball at ({ball_x}, {ball_y}) with center at ({center_x}, {center_y})")
    #
    #     # If the ball is overlapping or touching the boundary
    #     if distance_to_center >= (big_radius - self.radius):
    #         logging.info(f"Collision detected at distance: {distance_to_center} with boundary at {big_radius - self.radius}")
    #
    #         # Optionally play the collision sound
    #         if self.sound:
    #             pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))
    #             logging.debug("Collision sound played.")
    #
    #             # Reposition the ball just inside the boundary
    #             if velocity_magnitude == 0:
    #                 # Prevent division by zero by repositioning the ball directly without relying on its velocity
    #                 overlap = distance_to_center + self.radius - big_radius
    #                 self.pos_x -= (ball_x - center_x) / distance_to_center * overlap
    #                 self.pos_y -= (ball_y - center_y) / distance_to_center * overlap
    #             else:
    #                 while sqrt((center_x - self.pos_x) ** 2 + (center_y - self.pos_y) ** 2) > (
    #                         big_radius - self.radius):
    #                     step = 0.2  # This small step ensures that the ball moves just inside the boundary
    #                     self.pos_x += -self.vel_x * step / velocity_magnitude
    #                     self.pos_y += -self.vel_y * step / velocity_magnitude
    #                     logging.debug(f"Adjusting ball position to ({self.pos_x}, {self.pos_y}) to ensure it remains within boundary")
    #
    #         # Calculate normal vector from the circle's center to the ball
    #         normal_x, normal_y = ball_x - center_x, ball_y - center_y
    #         normal_magnitude = distance_to_center
    #         normal_x /= normal_magnitude
    #         normal_y /= normal_magnitude
    #
    #         # Calculate dot product of velocity and normal vector
    #         dot_product = normal_x * self.vel_x + normal_y * self.vel_y
    #
    #         # Reflect the velocity using the normal vector
    #         self.vel_x -= 2 * dot_product * normal_x
    #         self.vel_y -= 2 * dot_product * normal_y

    def handle_collision(self, center_pos_x, center_pos_y, boundary_radius):
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
            # # Calculate the direction vector from ball to center
            # direction_x = center_pos_x - ball_pos_x
            # direction_y = center_pos_y - ball_pos_y
            # direction_magnitude = sqrt(direction_x ** 2 + direction_y ** 2)
            # direction_x /= direction_magnitude
            # direction_y /= direction_magnitude
            #
            # # Adjust ball position until it is just inside the boundary
            # while distance_to_center >= (boundary_radius - self.radius):
            #     step = 0.5  # This small step ensures that the ball moves just inside the boundary
            #     self.pos_x += direction_x * step  # Adjust the step size if needed
            #     self.pos_y += direction_y * step
            #     distance_to_center = sqrt((center_pos_x - self.pos_x) ** 2 + (center_pos_y - self.pos_y) ** 2)
            #     logging.debug(
            #         f"Adjusting ball position to ({self.pos_x}, {self.pos_y}) to ensure it remains within boundary")
            #
            # # Reflect the velocity
            # dot_product = direction_x * self.vel_x + direction_y * self.vel_y
            # self.vel_x -= 2 * dot_product * direction_x
            # self.vel_y -= 2 * dot_product * direction_y
            # logging.debug(f"Ball velocity updated to ({self.vel_x}, {self.vel_y}) after reflection.")

    def update_motion(self, center_x, center_y, big_radius):
        self.vel_y += self.acc
        self.pos_x += self.vel_x
        self.pos_y -= self.vel_y
        logging.debug(
            f"Ball motion updated: position ({self.pos_x}, {self.pos_y}), velocity ({self.vel_x}, {self.vel_y})")

        # dx = self.pos_x - center_x
        # dy = self.pos_y - center_y
        # distance_from_center = sqrt(dx ** 2 + dy ** 2)
        # if distance_from_center > big_radius - self.radius:
        #     overlap = distance_from_center - (big_radius - self.radius)
        #     self.pos_x -= (dx / distance_from_center) * overlap
        #     self.pos_y -= (dy / distance_from_center) * overlap
        #     normal_x, normal_y = dx / distance_from_center, dy / distance_from_center
        #     dot_product = normal_x * self.vel_x + normal_y * self.vel_y
        #     self.vel_x -= 2 * dot_product * normal_x
        #     self.vel_y -= 2 * dot_product * normal_y
        #     logging.info(f"Ball adjusted due to boundary overlap at ({self.pos_x}, {self.pos_y})")

    # def update_track(self, frames, trail, fps):
    #     if trail:
    #         if not self.track or hypot(self.track[-1][0] - self.pos_x, self.track[-1][1] - self.pos_y) > 5:
    #             self.track.append((self.pos_x, self.pos_y))
    #             logging.debug(f"Track updated with new position ({self.pos_x}, {self.pos_y})")
    #         if len(self.track) > fps * 5:
    #             self.track.pop(0)
    #             logging.debug("Oldest track point removed due to size limit.")
    #     else:
    #         self.track.clear()
    #         logging.debug("Track cleared as trailing is disabled.")

    def update_track(self, frames, trail, fps):
        every = 2
        period = 5
        if frames % every == 0 and trail:
            self.track.append((self.pos_x, self.pos_y))
        if not trail:
            self.track.clear()
        elif len(self.track) > fps * period / every:
            self.track.pop(0)


class BallPool:
    def __init__(self, size):
        self.size = size
        self.pool = [Ball("Default", (0, 255, 255), 10, 1, 1, -100, -100, "") for _ in range(size)]
        self.available = self.pool.copy()
        self.active_balls = []  # List to track active balls

    def acquire(self, name, color, radius, vel_x, vel_y, pos_x, pos_y, sound):
        if not self.available:
            raise Exception("No balls available in the pool")
        ball = self.available.pop()
        ball.reset(name, color, radius, vel_x, vel_y, pos_x, pos_y, sound)
        #self.active_balls.append(ball)
        return ball

    def release(self, ball):
        ball.reset("Default", (0, 255, 255), 10, 1, 1, -100, -100, "")
        self.available.append(ball)
        self.active_balls.remove(ball)  # Remove from active list when released


class BigCircle:
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, self.center_x, self.center_y, self.radius, self.color)
