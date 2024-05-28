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

    def update_motion_trace(self, current_frame, enable_trail, frames_per_second):
        frame_interval = 2
        trail_duration = 1  # in seconds

        if current_frame % frame_interval == 0 and enable_trail:
            self.track.append((self.pos_x, self.pos_y))

        if not enable_trail:
            self.track.clear()
        elif len(self.track) > frames_per_second * trail_duration / frame_interval:
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
        ball.reset("Default", WHITEST, 10, 1, 1, -100, -100, "")
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
