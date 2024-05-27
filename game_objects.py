from math import sqrt, hypot

import pygame
import pygame.gfxdraw

from constants import *


class Ball:
    balls = []

    def __init__(self, name, color, radius, vel_x, pos_x, pos_y, sound):
        self.name = name
        self.color = color
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sound = sound
        self.acc = GRAVITY  # Acceleration, can be set accordingly
        self.thickness = 0  # Border thickness for drawing
        self.track = []
        # Ball.balls.append(self)

    def reset(self, name, color, radius, vel_x, pos_x, pos_y, sound="audio/golf_ball.wav"):
        self.name = name
        self.color = color
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sound = sound
        self.acc = 0
        self.track.clear()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius, self.thickness)

    def handle_collision(self, center_x, center_y, big_radius):
        velocity_magnitude = sqrt(self.vel_x ** 2 + self.vel_y ** 2)
        ball_x, ball_y = self.pos_x, self.pos_y

        # Calculate the distance from the ball to the circle's center
        distance_to_center = sqrt((center_x - ball_x) ** 2 + (center_y - ball_y) ** 2)

        # If the ball is overlapping or touching the boundary
        if distance_to_center >= (big_radius - self.radius):
            # Optionally play the collision sound
            if self.sound:
                pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))

                # Reposition the ball just inside the boundary
                if velocity_magnitude == 0:
                    # Prevent division by zero by repositioning the ball directly without relying on its velocity
                    overlap = distance_to_center + self.radius - big_radius
                    self.pos_x -= (ball_x - center_x) / distance_to_center * overlap
                    self.pos_y -= (ball_y - center_y) / distance_to_center * overlap
                else:
                    while sqrt((center_x - self.pos_x) ** 2 + (center_y - self.pos_y) ** 2) > (
                            big_radius - self.radius):
                        step = 0.2  # This small step ensures that the ball moves just inside the boundary
                        self.pos_x += -self.vel_x * step / velocity_magnitude
                        self.pos_y += -self.vel_y * step / velocity_magnitude

            # Calculate normal vector from the circle's center to the ball
            normal_x, normal_y = ball_x - center_x, ball_y - center_y
            normal_magnitude = distance_to_center
            normal_x /= normal_magnitude
            normal_y /= normal_magnitude

            # Calculate dot product of velocity and normal vector
            dot_product = normal_x * self.vel_x + normal_y * self.vel_y

            # Reflect the velocity using the normal vector
            self.vel_x -= 2 * dot_product * normal_x
            self.vel_y -= 2 * dot_product * normal_y

    def update_motion(self, center_x, center_y, big_radius):
        self.vel_y += self.acc
        self.pos_x += self.vel_x
        self.pos_y -= self.vel_y

        dx = self.pos_x - center_x
        dy = self.pos_y - center_y
        distance_from_center = sqrt(dx ** 2 + dy ** 2)
        if distance_from_center > big_radius - self.radius:
            overlap = distance_from_center - (big_radius - self.radius)
            self.pos_x -= (dx / distance_from_center) * overlap
            self.pos_y -= (dy / distance_from_center) * overlap
            normal_x, normal_y = dx / distance_from_center, dy / distance_from_center
            dot_product = normal_x * self.vel_x + normal_y * self.vel_y
            self.vel_x -= 2 * dot_product * normal_x
            self.vel_y -= 2 * dot_product * normal_y

    def update_track(self, frames, trail, fps):
        if trail:
            if not self.track or hypot(self.track[-1][0] - self.pos_x, self.track[-1][1] - self.pos_y) > 5:
                self.track.append((self.pos_x, self.pos_y))
            if len(self.track) > fps * 5:
                self.track.pop(0)
        else:
            self.track.clear()


class BallPool:
    def __init__(self, size):
        self.size = size
        self.pool = [Ball("Default", (128, 128, 128), 10, 1, -100, -100, "") for _ in range(size)]
        self.available = self.pool.copy()
        self.active_balls = []  # List to track active balls

    def acquire(self, name, color, radius, vel_x, pos_x, pos_y, sound):
        if not self.available:
            raise Exception("No balls available in the pool")
        ball = self.available.pop()
        ball.reset(name, color, radius, vel_x, pos_x, pos_y, sound)
        self.active_balls.append(ball)
        return ball

    def release(self, ball):
        ball.reset("Default", (128, 128, 128), 10, 1, -100, -100, "")
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
