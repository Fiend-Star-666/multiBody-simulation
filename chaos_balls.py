from events import *
from game_objects import *
from graphics import *
from physics import *

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
    collision_sound = "audio/golf_ball.wav"

    red_ball = ball_pool.acquire("Red Ball", RED, 8, 5, WIDTH // 2 - HEIGHT // 2 + 10, HEIGHT // 2, collision_sound)
    red_ball.vel_y = -5
    ball_pool.active_balls.append(red_ball)
    # Uncomment and use the following if you want more balls active initially green_ball = ball_pool.acquire("Green
    # Ball", GREEN, 8, 0, WIDTH // 2 + HEIGHT // 2 - 10, HEIGHT // 2, collision_sound) green_ball.vel_y = 5
    # green_ball.vel_x = -5

    # velvet_ball = ball_pool.acquire("Velvet Ball", VELVET, 8, 10, WIDTH // 2, HEIGHT // 2 - HEIGHT // 2 + 10,
    # collision_sound) gold_ball = ball_pool.acquire("Gold Ball", MAGENTA, 8, 2, WIDTH // 2, HEIGHT // 2 + HEIGHT //
    # 2 - 10, collision_sound)


# Initial screen before simulation starts
while not start_sim:
    screen.fill(DEEP_BLUE)
    draw_background(screen, background)
    start_sim = handle_events(pygame.event.get(), 'start_sim')
    pygame.display.update()  # Update the display

# Create initial balls once the simulation starts
create_initial_balls()  # Ensure you've defined and passed the ball_pool

# Main simulation loop
frames = 0
while True:
    screen.fill(DEEP_BLUE)
    draw_big_circle(screen, big_circle)  # Draw the big circle

    events = pygame.event.get()
    pause, trail = handle_events(events, 'runtime', additional_params={'pause': pause, 'trail': trail})

    if not pause:
        for ball in ball_pool.active_balls:  # Use active balls from the ball pool
            ball.handle_collision(WIDTH // 2, HEIGHT // 2, HEIGHT // 2)
            ball.update_motion(WIDTH // 2, HEIGHT // 2, HEIGHT // 2)
            ball.update_track(frames, trail, FPS)

    draw_balls(screen)  # Ensure this function draws only active balls
    update_display(clock, FPS)
    frames += 1
