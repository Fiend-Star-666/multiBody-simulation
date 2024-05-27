import pygame
import sys
import math

pygame.init()

window = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()

outer_circle_radius = 250
outer_circle_pos = [375, 375]
inner_circle_radius = 25
inner_circle_pos = [375, 200]
inner_circle_vel = [2, 1]
inner_circle_grav = 0.2
inner_radius_change = 5
outer_radius_change = 0
radius_change = inner_radius_change + outer_radius_change

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the distance between the inner and outer circles
    distance = math.sqrt((inner_circle_pos[0] - outer_circle_pos[0]) ** 2 + (inner_circle_pos[1] - outer_circle_pos[1]) ** 2)

    # Check for collisions between the outer perimeter of the outer circle and the outer perimeter of the inner circle
    if distance + inner_circle_radius >= outer_circle_radius:
        # Undo last move
        inner_circle_pos[0] -= inner_circle_vel[0]
        inner_circle_pos[1] -= inner_circle_vel[1]

        angle = math.atan2(inner_circle_pos[1] - outer_circle_pos[1], inner_circle_pos[0] - outer_circle_pos[0])
        wall_angle = math.degrees(angle)

        # Get the point of contact between the outer and inner circles
        contact_point_x = outer_circle_pos[0] + outer_circle_radius * math.cos(angle)
        contact_point_y = outer_circle_pos[1] + outer_circle_radius * math.sin(angle)

        # Get the inner circle's current angle
        ball_angle = math.degrees(math.atan2(inner_circle_vel[1], inner_circle_vel[0]))

        # Get the inner circle's new angle
        new_angle = (2 * wall_angle) - ball_angle - 180

        # Get the speed of the inner circle
        new_velocity_magnitude = math.sqrt(inner_circle_vel[0] ** 2 + inner_circle_vel[1] ** 2)

        # Calculate the new velocity based on the angle
        inner_circle_vel[0] = new_velocity_magnitude * math.cos(math.radians(new_angle))
        inner_circle_vel[1] = new_velocity_magnitude * math.sin(math.radians(new_angle))

    # Account for change in radius
    inner_circle_pos[0] += (inner_circle_vel[0] + radius_change) if inner_circle_vel[0] >= 0 else (inner_circle_vel[0] - radius_change)
    inner_circle_pos[1] += (inner_circle_vel[1] + radius_change) if inner_circle_vel[1] >= 0 else (inner_circle_vel[1] - radius_change)

    # Change the radius
    inner_circle_radius += inner_radius_change
    outer_circle_radius += outer_radius_change

    # Adjust the inner circle's velocity based on gravity
    inner_circle_vel[1] += inner_circle_grav

    # Add the velocity to the inner circle's position
    inner_circle_pos[0] += inner_circle_vel[0]
    inner_circle_pos[1] += inner_circle_vel[1]

    if inner_circle_radius >= outer_circle_radius:
        print("TOO BIG")

    window.fill(0)
    pygame.draw.circle(window, (255, 255, 255), inner_circle_pos, inner_circle_radius)
    pygame.draw.circle(window, (255, 255, 255), outer_circle_pos, outer_circle_radius, 3)
    pygame.display.update()
    clock.tick(60)
