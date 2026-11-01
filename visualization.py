import pygame
from drone import Drone
from environment import Environment
from mission_controller import MissionController
import pygame.freetype

def draw_drone(screen, drone, cell_size, offset_x=0, offset_y=0):
    x, y = drone.get_position()

    x_c = x * cell_size + cell_size // 2 + offset_x
    y_c = y * cell_size + cell_size // 2 + offset_y

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

def draw_goal(screen, goal, cell_size, offset_x=0, offset_y=0):
    x, y = goal

    x_c = x * cell_size + cell_size // 2 + offset_x
    y_c = y * cell_size + cell_size // 2 + offset_y

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


def draw_controls(screen, title_font, controls_font):
    # Colors
    PANEL_COLOR = (40, 46, 53)
    TITLE_COLOR = (235, 243, 247)
    LABEL_COLOR = (160, 175, 190)

    # Rounded background panel
    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        (15, 375, 465, 110),
        border_radius=10
    )

    # Heading
    title_font.render_to(
        screen,
        (30, 390),
        "CONTROLS",
        TITLE_COLOR
    )

    # Divider
    pygame.draw.line(
        screen,
        (75, 85, 95),
        (30, 415),
        (465, 415),
        1
    )

    # Left column
    controls_font.render_to(screen, (30, 425), "SPACE  -  Pause / Resume", LABEL_COLOR)
    controls_font.render_to(screen, (30, 445), "LMB  -  Add obstacle", LABEL_COLOR)
    controls_font.render_to(screen, (30, 465), "RMB  -  Remove obstacle", LABEL_COLOR)

    # Right column
    controls_font.render_to(screen, (255, 425), "S  -  Start", LABEL_COLOR)
    controls_font.render_to(screen, (255, 445), "R  -  Reset", LABEL_COLOR)
    controls_font.render_to(screen, (255, 465), "A  -  Switch Algorithm", LABEL_COLOR)

def run_simulation():
    pygame.init()

    screen = pygame.display.set_mode((750, 600))
    pygame.display.set_caption("Autonomous Drone Mission Simulator")

    clock = pygame.time.Clock()

    running = True

    GRID_WIDTH = 7
    GRID_HEIGHT = 5
    CELL_SIZE = 60

    environment = Environment(GRID_WIDTH, GRID_HEIGHT)

    environment.add_obstacle((2, 0))
    environment.add_obstacle((2, 1))
    environment.add_obstacle((2, 2))
    environment.add_obstacle((2, 3))

    START_POSITION = (0, 0)
    drone = Drone(START_POSITION)

    goal = (5, 4)

    mission = MissionController(drone, environment)

    MOVE_DELAY = 500
    last_move = pygame.time.get_ticks()

    title_font = pygame.freetype.SysFont("Helvetica Neue", 15, bold=True)
    label_font = pygame.freetype.SysFont("Helvetica Neue", 14)
    value_font = pygame.freetype.SysFont("Helvetica Neue", 18, bold=True)
    coordinate_font = pygame.freetype.SysFont("Helvetica Neue", 12)
    controls_title_font = pygame.freetype.SysFont("Helvetica Neue", 14, bold=True)
    controls_font = pygame.freetype.SysFont("Helvetica Neue", 13)

    GRID_OFFSET_X = 45
    GRID_OFFSET_Y = 45

    STATUS_COLORS = {
        "IDLE": (235, 243, 247),
        "MOVING": (66, 201, 145),
        "PAUSED": (245, 200, 100),
        "COMPLETED": (66, 201, 145),
        "FAILED": (239, 115, 115)
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mission.state == "MOVING":
                        mission.pause_mission()
                    elif mission.state == "PAUSED":
                        mission.resume_mission()
                        last_move = pygame.time.get_ticks()
                elif event.key == pygame.K_r:
                    mission.reset_mission()
                    drone.move_to(START_POSITION)
                    last_move = pygame.time.get_ticks()
                elif event.key == pygame.K_s:
                    if mission.state == "IDLE":
                        mission.start_mission(goal)
                        last_move = pygame.time.get_ticks()
                elif event.key == pygame.K_a:
                    if mission.state == "IDLE":
                        if mission.algorithm == "BFS":
                            mission.algorithm = "A*"
                        else:
                            mission.algorithm = "BFS"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                x_grid = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                y_grid = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

                previous_state = mission.state

                if event.button == 1:
                    if environment.is_valid_move((x_grid, y_grid)) and (x_grid, y_grid) != drone.get_position() and (x_grid, y_grid) != goal:
                        environment.add_obstacle((x_grid, y_grid))

                        if mission.state == "MOVING" or mission.state == "PAUSED":
                            mission.start_mission(goal)
                            if previous_state == "PAUSED" and mission.state == "MOVING":
                                mission.pause_mission()
                elif event.button == 3:
                    if (x_grid, y_grid) in environment.obstacles:
                        environment.obstacles.discard((x_grid, y_grid))
                        
                        if mission.state == "MOVING" or mission.state == "PAUSED":
                            mission.start_mission(goal)
                            if previous_state == "PAUSED" and mission.state == "MOVING":
                                mission.pause_mission()

        current_time = pygame.time.get_ticks()

        if mission.state == "MOVING" and current_time - last_move >= MOVE_DELAY:
            mission.update()
            last_move = current_time

        DARK_GRAY = (30, 30, 30)
        screen.fill(DARK_GRAY)

        pygame.draw.rect(
            screen,
            (38, 49, 58),
            (15, 15, 465, 345),
            border_radius=10
        )

        for x, y in environment.obstacles:
            pygame.draw.rect(
                screen,
                (220, 60, 60),
                (x * CELL_SIZE + GRID_OFFSET_X, y * CELL_SIZE + GRID_OFFSET_Y, CELL_SIZE, CELL_SIZE),
                0
            )   

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):        
                pygame.draw.rect(
                    screen,
                    (80, 100, 120),
                    (x * CELL_SIZE + GRID_OFFSET_X, y * CELL_SIZE + GRID_OFFSET_Y, CELL_SIZE, CELL_SIZE),
                    1
                ) 
        
        for x in range(GRID_WIDTH):
            text = str(x)

            text_rect = coordinate_font.get_rect(text)

            x_center = GRID_OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2

            label_center_y = (15 + GRID_OFFSET_Y) // 2

            coordinate_font.render_to(
                screen,
                (x_center - text_rect.width // 2, label_center_y - text_rect.height),
                text,
                (160, 175, 190)
            )

        for y in range(GRID_HEIGHT):
            text = str(y)

            text_rect = coordinate_font.get_rect(text)

            y_center = GRID_OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2

            label_center_x = (15 + GRID_OFFSET_X) // 2

            coordinate_font.render_to(
                screen,
                (label_center_x - text_rect.width // 2, y_center - text_rect.height // 2),
                text,
                (160, 175, 190)
            )
        
        pygame.draw.rect(
            screen,
            (40, 46, 53),
            (495, 15, 240, 570),
            border_radius=10
        )

        for x, y in mission.path[:-1]:
            x_c = x * CELL_SIZE + CELL_SIZE // 2 + GRID_OFFSET_X
            y_c = y * CELL_SIZE + CELL_SIZE // 2 + GRID_OFFSET_Y

            pygame.draw.circle(
                screen,
                (245, 200, 100),
                (x_c, y_c),
                5
            )

        draw_goal(screen, goal, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)
            
        draw_drone(screen, drone, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)

        draw_controls(screen, controls_title_font, controls_font)

        title_font.render_to(
            screen,
            (510, 35),
            "MISSION DASHBOARD",
            (235, 243, 247)
        )

        pygame.draw.line(
            screen,
            (75, 85, 95),
            (510, 70),
            (670, 70),
            1
        )

        label_font.render_to(
            screen,
            (510, 90),
            "STATUS",
            (160, 175, 190)
        )

        status_color = STATUS_COLORS[mission.state]

        value_font.render_to(
            screen,
            (510, 115),
            mission.state,
            status_color
        )

        position_text = f"{drone.get_position()}"

        label_font.render_to(
            screen,
            (510, 155),
            "DRONE POSITION",
            (160, 175, 190)
        )

        value_font.render_to(
            screen,
            (510, 180),
            position_text,
            (235, 243, 247)
        )

        label_font.render_to(
            screen,
            (510, 220),
            "DESTINATION",
            (160, 175, 190)
        )

        value_font.render_to(
            screen,
            (510, 245),
            f"{goal}",
            (235, 243, 247)
        )

        label_font.render_to(
            screen,
            (510, 285),
            "ALGORITHM",
            (160, 175, 190)
        )

        value_font.render_to(
            screen,
            (510, 310),
            mission.algorithm,
            (235, 243, 247)
        )
        
        label_font.render_to(
            screen,
            (510, 350),
            "REMAINING STEPS",
            (160, 175, 190)
        )

        remaining_steps = max(0, len(mission.path) - 1)
        value_font.render_to(
            screen,
            (510, 375),
            f"{remaining_steps}",
            (235, 243, 247)
        )

        label_font.render_to(
            screen,
            (510, 415),
            "NODES EXPLORED",
            (160, 175, 190)
        )

        value_font.render_to(
            screen,
            (510, 440),
            str(mission.nodes_explored),
            (235, 243, 247)
        )

        label_font.render_to(
            screen,
            (510, 480),
            "SEARCH TIME",
            (160, 175, 190)
        )

        value_font.render_to(
            screen,
            (510, 505),
            f"{mission.search_time_ms:.4f} ms",
            (235, 243, 247)
        )
        
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_simulation()