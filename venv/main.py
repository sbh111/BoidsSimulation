import pygame
import random
import time
from flock import Flock
from quad_tree import *

def main():
    pygame.init()
    display = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Boids Simulation")
    random.seed(time.time())

    flock = Flock(100)
    clock = pygame.time.Clock()
    while True:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((0, 0, 50))

        flock.draw()

        pygame.display.flip()
main()
