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
        self.thickness = 6  # Border thickness for drawing
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
        self.acc = GRAVITY
        self.track.clear()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius, self.thickness)

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

    def update_track(self, frames, trail, fps):
        every = 2
        period = 1
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
        # self.active_balls.append(ball)
        return ball

    def release(self, ball):
        ball.reset("Default", (0, 255, 255), 10, 1, 1, -100, -100, "")
        self.available.append(ball)
        self.active_balls.remove(ball)  # Remove from active list when released

goldball = Ball("gold ball", (255, 72, 0), 8, 0, WIDTH // 2 + bigr - 10, HEIGHT // 2, "golf_ball.wav")
goldball.vely = 5

class BigCircle:
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, self.center_x, self.center_y, self.radius, self.color)
