import pygame
from drone import Drone
from environment import Environment
from pathfinding import bfs

def draw_drone(screen, drone, cell_size):
    x, y = drone.get_position()

    x_c = x * cell_size + cell_size // 2
    y_c = y * cell_size + cell_size // 2

    # Draw at 3x resolution for smoother edges
    SCALE = 3
    size = cell_size * SCALE

    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    cx = size // 2
    cy = size // 2

    def point(x, y):
        return (cx + x * SCALE, cy + y * SCALE)

    # Colors
    ARM_COLOR = (113, 141, 170)
    ROTOR_COLOR = (93, 197, 239)
    ROTOR_FILL = (36, 60, 80)
    HUB_COLOR = (200, 235, 250)
    BODY_COLOR = (50, 150, 255)
    BODY_BORDER = (181, 221, 249)
    ARROW_COLOR = (221, 245, 255)

    # 1. Draw diagonal arms
    pygame.draw.line(
        surface, ARM_COLOR,
        point(-18, -18), point(18, 18),
        7 * SCALE
    )

    pygame.draw.line(
        surface, ARM_COLOR,
        point(18, -18), point(-18, 18),
        7 * SCALE
    )

    # 2. Draw four rotors
    rotor_positions = [
        (-18, -18),
        (18, -18),
        (-18, 18),
        (18, 18)
    ]

    for rx, ry in rotor_positions:
        center = point(rx, ry)

        # Dark rotor interior
        pygame.draw.circle(
            surface, ROTOR_FILL,
            center, 10 * SCALE
        )

        # Cyan rotor outline
        pygame.draw.circle(
            surface, ROTOR_COLOR,
            center, 10 * SCALE,
            2 * SCALE
        )

        # Propeller blades
        pygame.draw.line(
            surface, ROTOR_COLOR,
            point(rx - 7, ry + 5),
            point(rx + 7, ry - 5),
            3 * SCALE
        )

        # Rotor hub
        pygame.draw.circle(
            surface, HUB_COLOR,
            center, 3 * SCALE
        )

    # 3. Draw medium-sized rounded central body
    body = pygame.Rect(
        cx - 10.5 * SCALE,
        cy - 13.5 * SCALE,
        21 * SCALE,
        27 * SCALE
    )

    pygame.draw.rect(
        surface, BODY_COLOR,
        body, border_radius=7 * SCALE
    )

    pygame.draw.rect(
        surface, BODY_BORDER,
        body, 2 * SCALE,
        border_radius=7 * SCALE
    )

    # 4. Draw forward-facing arrow
    pygame.draw.polygon(
        surface, ARROW_COLOR,
        [
            point(0, -11),
            point(-6, -2),
            point(6, -2)
        ]
    )

    # 5. Smoothly scale the drone with some margin
    DRONE_SCALE = 0.80

    drone_size = int(cell_size * DRONE_SCALE)

    surface = pygame.transform.smoothscale(
        surface,
        (drone_size, drone_size)
    )

    # 6. Center the smaller drone inside its grid cell
    screen.blit(
        surface,
        (
            x_c - drone_size // 2,
            y_c - drone_size // 2
        )
    )

def draw_goal(screen, goal, cell_size):
    x, y = goal

    x_c = x * cell_size + cell_size // 2
    y_c = y * cell_size + cell_size // 2

    # Colors
    POLE_COLOR = (190, 200, 210)
    FLAG_COLOR = (50, 200, 120)

    # Draw flagpole
    pygame.draw.line(
        screen,
        POLE_COLOR,
        (x_c - 10, y_c - 20),
        (x_c - 10, y_c + 20),
        3
    )

    # Draw triangular green flag
    pygame.draw.polygon(
        screen,
        FLAG_COLOR,
        [
            (x_c - 10, y_c - 20),
            (x_c + 18, y_c - 11),
            (x_c - 10, y_c - 2)
        ]
    )

    # Draw base
    pygame.draw.line(
        screen,
        POLE_COLOR,
        (x_c - 17, y_c + 20),
        (x_c - 3, y_c + 20),
        3
    )


def run_simulation():
    pygame.init()

    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Autonomous Drone Mission Simulator")

    clock = pygame.time.Clock()

    running = True

    GRID_WIDTH = 7
    GRID_HEIGHT = 5
    CELL_SIZE = 60

    environment = Environment(GRID_WIDTH, GRID_HEIGHT)

    environment.add_obstacle((3, 1))
    environment.add_obstacle((3, 2))
    environment.add_obstacle((3, 3))

    drone = Drone((2, 3))

    goal = (5, 4)

    path = bfs(drone.get_position(), goal, environment)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        DARK_GRAY = (30, 30, 30)
        screen.fill(DARK_GRAY)

        for x, y in environment.obstacles:
            pygame.draw.rect(
                screen,
                (220, 60, 60),
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                0
            )   

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):        
                pygame.draw.rect(
                    screen,
                    (80, 100, 120),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1
                ) 

        for x, y in path[:-1]:
            x_c = x * CELL_SIZE + CELL_SIZE // 2
            y_c = y * CELL_SIZE + CELL_SIZE // 2

            pygame.draw.circle(
                screen,
                (245, 200, 100),
                (x_c, y_c),
                5
            )

        draw_goal(screen, goal, CELL_SIZE)
            
        draw_drone(screen, drone, CELL_SIZE)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_simulation()