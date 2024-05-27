import pygame
from math import sqrt
from constants import GRAVITY, FPS, WIDTH, HEIGHT
import pygame.gfxdraw


class Ball:
    balls = []

    def __init__(self, name, color, radius, thicc, posx, posy, sound="metalmicrowave.wav"):
        self.name = name
        self.color = color
        self.radius = radius
        self.thicc = thicc
        self.posx = posx
        self.posy = posy
        self.sound = f"audio/{sound}"
        self.velx = 0
        self.vely = 0
        self.acc = GRAVITY / FPS
        self.track = []
        Ball.balls.append(self)

    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, int(self.posx), int(self.posy), self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, int(self.posx), int(self.posy), self.radius, self.color)
        # pygame.draw.circle(screen, self.color, (int(self.posx), int(self.posy)), self.radius, self.thicc)

    def handle_collision(self, centx, centy, bigr):
        vel = sqrt(self.velx ** 2 + self.vely ** 2)
        x, y = centx, centy
        ballx, bally = self.posx, self.posy
        velx, vely = self.velx, self.vely
        center_to_ball = sqrt((x - ballx) ** 2 + (y - bally) ** 2)

        if center_to_ball >= (bigr - self.radius):
            pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))
            while sqrt((x - self.posx) ** 2 + (y - self.posy) ** 2) > (bigr - self.radius):
                step = 0.2
                self.posx += -self.velx * step / vel
                self.posy -= -self.vely * step / vel

            normal = ballx - x, bally - y
            normal_mag = center_to_ball
            nx, ny = normal[0] / normal_mag, normal[1] / normal_mag

            d = velx, -vely
            reflected = d[0] - 2 * (nx * d[0] + ny * d[1]) * nx, d[1] - 2 * (nx * d[0] + ny * d[1]) * ny

            self.velx = reflected[0]
            self.vely = -reflected[1]

    def update_motion(self):
        self.velx += 0
        self.vely += self.acc
        self.posx += self.velx
        self.posy -= self.vely

    def update_track(self, frames, trail, fps):
        every = 2
        period = 5
        if frames % every == 0 and trail:
            self.track.append((self.posx, self.posy))
        if not trail:
            self.track.clear()
        elif len(self.track) > fps * period / every:
            self.track.pop(0)


# Create balls
bigr = HEIGHT // 2
redball = Ball("red ball", (245, 170, 10), 8, 0, WIDTH // 2 - bigr + 10, HEIGHT // 2, "golf_ball.wav")
redball.vely = -5

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
