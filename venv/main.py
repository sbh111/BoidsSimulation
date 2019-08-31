import pygame
from flock import Flock

def main():
    pygame.init()
    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Boids Simulation")

    flock = Flock(10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((0, 0, 0))

        flock.draw()

        pygame.display.flip()
main()
