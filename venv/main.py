import pygame
import random
import time
from flock import Flock

def main():
    pygame.init()
    display = pygame.display.set_mode((700, 600))
    random.seed(time.time())

    flock = Flock(100)
    clock = pygame.time.Clock()

    useTree = False
    showTree = False

    while True:

        clock.tick()
        fps = clock.get_fps()
        pygame.display.set_caption("Boids Simulation - Boids: {0} - FPS: {1}".format(len(flock.flock), int(fps)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                flock.insertBoid((pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN:
                if pygame.K_BACKSPACE:
                    flock.removeBoid()


        display.fill((10, 10, 60))
        flock.draw(useTree, showTree)
        pygame.display.flip()
main()
