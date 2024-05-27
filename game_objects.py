from math import sqrt

import pygame
import pygame.gfxdraw


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
        self.acc = 0  # Acceleration, can be set accordingly
        self.thickness = 0  # Border thickness for drawing
        self.track = []
        Ball.balls.append(self)

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
        distance_to_center = sqrt((center_x - ball_x) ** 2 + (center_y - ball_y) ** 2)

        if distance_to_center >= (big_radius - self.radius):
            pygame.mixer.Sound.play(pygame.mixer.Sound("audio/golf_ball.wav"))

            if velocity_magnitude > 0:  # Check to avoid division by zero
                while sqrt((center_x - self.pos_x) ** 2 + (center_y - self.pos_y) ** 2) > (big_radius - self.radius):
                    step = 0.2
                    self.pos_x += -self.vel_x * step / velocity_magnitude
                    self.pos_y -= -self.vel_y * step / velocity_magnitude

            normal_x = ball_x - center_x
            normal_y = ball_y - center_y
            normal_magnitude = distance_to_center
            normal_x /= normal_magnitude
            normal_y /= normal_magnitude

            incoming_velocity_x = self.vel_x
            incoming_velocity_y = self.vel_y
            dot_product = normal_x * incoming_velocity_x + normal_y * incoming_velocity_y

            reflected_velocity_x = incoming_velocity_x - 2 * dot_product * normal_x
            reflected_velocity_y = incoming_velocity_y - 2 * dot_product * normal_y

            self.vel_x = reflected_velocity_x
            self.vel_y = -reflected_velocity_y

    def handle_collision(self, center_x, center_y, big_radius):
        velocity_magnitude = sqrt(self.vel_x ** 2 + self.vel_y ** 2)
        ball_x, ball_y = self.pos_x, self.pos_y
        distance_to_center = sqrt((center_x - ball_x) ** 2 + (center_y - ball_y) ** 2)

        if distance_to_center >= (big_radius - self.radius):
            pygame.mixer.Sound.play(pygame.mixer.Sound("audio/golf_ball.wav"))

            if velocity_magnitude > 0:  # Check to avoid division by zero
                while sqrt((center_x - self.pos_x) ** 2 + (center_y - self.pos_y) ** 2) > (big_radius - self.radius):
                    step = 0.2
                    self.pos_x += -self.vel_x * step / velocity_magnitude
                    self.pos_y -= -self.vel_y * step / velocity_magnitude

            normal_x = ball_x - center_x
            normal_y = ball_y - center_y
            normal_magnitude = distance_to_center
            normal_x /= normal_magnitude
            normal_y /= normal_magnitude

            incoming_velocity_x = self.vel_x
            incoming_velocity_y = self.vel_y
            dot_product = normal_x * incoming_velocity_x + normal_y * incoming_velocity_y

            reflected_velocity_x = incoming_velocity_x - 2 * dot_product * normal_x
            reflected_velocity_y = incoming_velocity_y - 2 * dot_product * normal_y

            self.vel_x = reflected_velocity_x
            self.vel_y = -reflected_velocity_y

    def update_motion(self):
        self.vel_x += 0  # No horizontal acceleration
        self.vel_y += self.acc  # Vertical acceleration
        self.pos_x += self.vel_x
        self.pos_y -= self.vel_y

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
        self.pool = [Ball("", (0, 0, 0), 0, 0, 0, 0, "") for _ in range(size)]
        self.available = self.pool.copy()

    def acquire(self, name, color, radius, vel_x, pos_x, pos_y, sound):
        if not self.available:
            raise Exception("No balls available in the pool")
        ball = self.available.pop()
        ball.reset(name, color, radius, vel_x, pos_x, pos_y, sound)
        return ball

    def release(self, ball):
        ball.reset("", (0, 0, 0), 0, 0, 0, 0, "")
        self.available.append(ball)


class BigCircle:
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, self.center_x, self.center_y, self.radius, self.color)
