import pygame
from constants import *
from graphics import setup_screen, draw_background, draw_balls, update_display, draw_big_circle
from events import handle_events
from game_objects import Ball, BigCircle

# Initialize Pygame and set up the window
pygame.init()
screen = setup_screen(WIDTH, HEIGHT, WINDOW_POSITION)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()
background = pygame.image.load("img/start_img.png")
big_circle = BigCircle(WIDTH // 2, HEIGHT // 2, HEIGHT // 2, GREEN)

# Main loop flags
pause = False
start_sim = False
trail = True

# Initial screen before simulation starts
while not start_sim:
    screen.fill(DEEPBLUE)
    draw_background(screen, background)
    start_sim = handle_events(pygame.event.get(), 'start_sim')
    pygame.display.update()  # Update the display

# Main simulation loop
frames = 0
while True:
    screen.fill(DEEPBLUE)
    draw_big_circle(screen, big_circle)  # Draw the big circle

    handle_events(pygame.event.get(), 'runtime', additional_params={'pause': pause, 'trail': trail})

    if not pause:
        for ball in Ball.balls:
            ball.handle_collision(WIDTH // 2, HEIGHT // 2, HEIGHT // 2)
            ball.update_motion()
            ball.update_track(frames, trail, FPS)

    draw_balls(screen)
    update_display(clock, FPS)
    frames += 1