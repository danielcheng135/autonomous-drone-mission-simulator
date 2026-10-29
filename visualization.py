import pygame

def run_simulation():
    pygame.init()

    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Autonomous Drone Mission Simulator")

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        DARK_GRAY = (30, 30, 30)
        screen.fill(DARK_GRAY)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_simulation()