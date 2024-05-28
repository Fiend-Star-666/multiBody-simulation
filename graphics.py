import os
from math import cos, sin, atan2, radians, degrees, sqrt, tan

import pygame
from pygame import gfxdraw


def setup_screen(width, height, position):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % position
    return pygame.display.set_mode((width, height))


def draw_background(screen, background):
    screen.blit(background, (0, 0))


def load_background(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Failed to load the image at {image_path}: {e}")
        raise SystemExit(e)


def draw_balls(screen, ball_pool):
    for ball in ball_pool.active_balls:
        if len(ball.track) > 2:
            pygame.draw.aalines(screen, ball.color, False, ball.track, 2)
        ball.draw(screen)


def update_display(clock, fps):
    pygame.display.update()
    clock.tick(fps)


def draw_big_circle(screen, big_circle):
    big_circle.draw(screen)


def move(rotation, steps, position):
    """Move a point in a given direction by a certain number of steps."""
    x_position = cos(radians(rotation)) * steps + position[0]
    y_position = sin(radians(rotation)) * steps + position[1]
    return x_position, y_position


def draw_thick_line(screen, point1, point2, thickness, color):
    """Draw a thick line between two points."""
    angle = degrees(atan2(point1[1] - point2[1], point1[0] - point2[0]))
    vertices = [
        move(angle - 90, thickness, point1),
        move(angle + 90, thickness, point1),
        move(angle + 90, thickness, point2),
        move(angle - 90, thickness, point2)
    ]
    gfxdraw.aapolygon(screen, vertices, color)
    gfxdraw.filled_polygon(screen, vertices, color)


def draw_arrow(screen, color, line_color, start, end, thickness):
    """Draw an arrow from start to end point."""
    theta = atan2(start[1] - end[1], end[0] - start[0])
    pygame.draw.circle(screen, color, start, thickness)
    draw_thick_line(screen, start, end, thickness, line_color)

    # Drawing the arrowhead
    length = sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    height = length / 8
    base = height * tan(radians(32))
    bx, by = end[0] - height * cos(theta), end[1] - height * sin(theta)
    arrowhead_points = [
        (end[0] + 5 * cos(theta), end[1] - 5 * sin(theta)),
        (bx - base * sin(theta), by - base * cos(theta)),
        (bx + base * sin(theta), by + base * cos(theta))
    ]
    gfxdraw.aapolygon(screen, arrowhead_points, color)
    gfxdraw.filled_polygon(screen, arrowhead_points, color)
