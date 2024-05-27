import pygame
from constants import *
from graphics import setup_screen, draw_background, draw_balls, update_display, draw_big_circle, load_background
from events import handle_events
from game_objects import Ball, BigCircle, BallPool

# Initialize Pygame and set up the window
pygame.init()
screen = setup_screen(WIDTH, HEIGHT, WINDOW_POSITION)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()
background = load_background("img/start_img.png")
big_circle = BigCircle(WIDTH // 2, HEIGHT // 2, HEIGHT // 2, GREEN)

# Main loop flags
pause = False
start_sim = False
trail = True

# Initialize ball pool
pool_size = 10
ball_pool = BallPool(pool_size)

# Function to create initial balls
def create_initial_balls():
    red_ball = ball_pool.acquire("Red Ball", RED, 8, 0, WIDTH // 2 - HEIGHT // 2 + 10, HEIGHT // 2, "golf_ball.wav")
    red_ball.vel_y = -5

    green_ball = ball_pool.acquire("Green Ball", GREEN, 8, 0, WIDTH // 2 + HEIGHT // 2 - 10, HEIGHT // 2, "golf_ball.wav")
    green_ball.vel_y = 5

    velvet_ball = ball_pool.acquire("Velvet Ball", VELVET, 8, 0, WIDTH // 2, HEIGHT // 2 - HEIGHT // 2 + 10, "golf_ball.wav")
    velvet_ball.vel_x = 10

    gold_ball = ball_pool.acquire("Gold Ball", MAGENTA, 8, 0, WIDTH // 2, HEIGHT // 2 + HEIGHT // 2 - 10, "golf_ball.wav")
    gold_ball.vel_x = 2

    # mage_ball = ball_pool.acquire("Mage Ball", MAGENTA2, 8, 0, WIDTH // 2 - HEIGHT // 2 + 10, HEIGHT // 2 - HEIGHT // 2 + 10, "golf_ball.wav")
    # mage_ball.vel_x = 1
    # Add more balls as needed using ball_pool.acquire()...

# Initial screen before simulation starts
while not start_sim:
    screen.fill(DEEP_BLUE)
    draw_background(screen, background)
    start_sim = handle_events(pygame.event.get(), 'start_sim')
    pygame.display.update()  # Update the display

# Create initial balls once the simulation starts
create_initial_balls()

# Main simulation loop
frames = 0
while True:
    screen.fill(DEEP_BLUE)
    draw_big_circle(screen, big_circle)  # Draw the big circle

    events = pygame.event.get()
    pause, trail = handle_events(events, 'runtime', additional_params={'pause': pause, 'trail': trail})

    if not pause:
        for ball in Ball.balls:
            ball.handle_collision(WIDTH // 2, HEIGHT // 2, HEIGHT // 2)
            ball.update_motion()
            ball.update_track(frames, trail, FPS)

    draw_balls(screen)
    update_display(clock, FPS)
    frames += 1
