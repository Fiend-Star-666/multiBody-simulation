from events import *
from game_objects import *
from graphics import *
from physics import *

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame and set up the window
pygame.init()
screen = setup_screen(DISPLAY_WIDTH, DISPLAY_HEIGHT, WINDOW_POSITION)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()
background = load_background("img/start_img.png")
circleCentre = (CIRCLE_WIDTH // 2, CIRCLE_HEIGHT // 2)
big_circle_radius = CIRCLE_HEIGHT // 2
big_circle = BigCircle(circleCentre[0], circleCentre[1], big_circle_radius, BLUISH_WHITE)
logging.debug("Game initialized with main window and big circle setup.")

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
    logging.debug("Creating initial balls.")
    ball_radius = 10

    red_ball = ball_pool.acquire("Red Ball", RED, ball_radius, 5, -5, circleCentre[0] - circleCentre[1] + ball_radius,
                                 big_circle_radius, collision_sound)
    ball_pool.active_balls.append(red_ball)
    logging.info("Red ball acquired from pool and initialized.")

    gold_ball = ball_pool.acquire("GOLDEN Ball", GOLDEN, ball_radius, -5, 5,
                                  circleCentre[0] + circleCentre[1] - ball_radius,
                                  big_circle_radius, collision_sound)
    ball_pool.active_balls.append(gold_ball)
    logging.info("GOLDEN ball acquired from pool and initialized.")


# Initial screen before simulation starts
while not start_sim:
    screen.fill(DEEP_BLUE)
    draw_background(screen, background)
    start_sim = handle_events(pygame.event.get(), 'start_sim')
    pygame.display.update()  # Update the display
    logging.debug("Waiting for simulation start.")

# Create initial balls once the simulation starts
create_initial_balls()

# Main simulation loop
frames = 0
while True:
    screen.fill(DEEP_BLUE)
    draw_big_circle(screen, big_circle)  # Draw the big circle
    logging.debug("Main simulation loop running.")

    events = pygame.event.get()
    pause, trail = handle_events(events, 'runtime', additional_params={'pause': pause, 'trail': trail})

    if not pause:
        for i, ball in enumerate(ball_pool.active_balls):
            ball.handle_boundary_collision(circleCentre[0], circleCentre[1], big_circle_radius)
            for other in ball_pool.active_balls[i + 1:]:
                ball.handle_ball_collision(other)
            ball.update_motion()
            ball.update_track(frames, trail, FPS)

    draw_balls(screen, ball_pool)  # Ensure this function draws only active balls
    update_display(clock, FPS)
    frames += 1
