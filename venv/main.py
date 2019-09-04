import pygame
import random
import time
from flock import Flock
from quad_tree import *

def main():
    pygame.init()
    display = pygame.display.set_mode((800, 800))
    random.seed(time.time())

    flock = Flock(100)
    clock = pygame.time.Clock()

    while True:

        clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption("Boids Simulation - FPS: {}".format(fps))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((10, 10, 60))

        #FIXME: teh quadtree seems to be returning points because it works with points internally
        # so make sure to return the point data for a query
        flock.draw(False)

        pygame.display.flip()
main()
