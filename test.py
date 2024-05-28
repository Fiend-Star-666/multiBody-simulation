import pygame
from pygame.math import Vector2

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CAPTION = "bouncing ring inside ring"
INITIAL_LINE_WIDTH = 5
INITIAL_HUE = 80
COLOR_BLACK = pygame.Color(0, 0, 0)
SIMULATION_GROWTH_RATE = 30
HUE_SPEED = 10

large_ring = {
    "center": Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
    "radius": SCREEN_HEIGHT * 3 / 8,
    "hue": INITIAL_HUE,
    "width": INITIAL_LINE_WIDTH * 2,
}


def initial_ring():
    return {
        "center": Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        "radius": 10,
        "hue": INITIAL_HUE,
        "width": INITIAL_LINE_WIDTH,
        "speed": Vector2(10.0, 0.0),
        "grow": 0,
    }


def get_color_from_hue(hue):
    color = pygame.Color(0, 0, 0, 255)
    color.hsva = (hue % 360, 100, 100, 100)
    return color


def init_screen(caption=""):
    pygame.display.set_caption(caption)
    pygame.font.init()
    return


def update_ring(ring: dict, g=0.1):
    ring["speed"] += (0, g)
    ring["center"] += ring["speed"]
    if ring["grow"] > 0:
        ring["radius"] += 1
        ring["grow"] -= 1


def draw_ring(ring: dict, surface=SCREEN):
    color = get_color_from_hue(ring["hue"])
    pygame.draw.circle(surface, color, ring["center"], ring["radius"], ring["width"])


def is_collision(l_ring, b_ring):
    if b_ring["grow"] > 0:
        return False
    point_l = l_ring["center"]
    point_b = b_ring["center"]
    distance = (point_b - point_l).length()
    separation = l_ring["radius"] - l_ring["width"] - b_ring["radius"]
    return separation < distance


def bounce_ring(l_ring, b_ring):
    # mirror the bouncing ring speed around the normal
    normal = (l_ring["center"] - b_ring["center"]).normalize()
    b_ring["speed"].reflect_ip(normal)


def process_collision(l_ring, b_ring):
    if is_collision(l_ring, b_ring):
        bounce_ring(l_ring, b_ring)

        # if there's no room to allocate the ring
        # current simulation ends, and we move to the next one
        future_ring = b_ring
        update_ring(future_ring)
        if is_collision(l_ring, future_ring):
            l_ring["width"] += SIMULATION_GROWTH_RATE
            l_ring["hue"] = INITIAL_HUE
            return initial_ring()

        # Increase radius and update colors
        b_ring["grow"] = 10
        b_ring["hue"] = (b_ring["hue"] + HUE_SPEED) % 360
        l_ring["hue"] = b_ring["hue"]

    return b_ring


def main():
    init_screen(CAPTION)
    clock = pygame.time.Clock()
    b_ring = initial_ring()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        SCREEN.fill(COLOR_BLACK)
        update_ring(b_ring)
        b_ring = process_collision(large_ring, b_ring)
        draw_ring(large_ring)
        draw_ring(b_ring)

        # Terminate main loop if we ran out of space
        if large_ring["width"] > large_ring["radius"]:
            running = False

        clock.tick(60)
        pygame.display.flip()

    # End main()
    pygame.quit()
    return


if __name__ == "__main__":
    main()
