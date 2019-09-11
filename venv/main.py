import pygame
import random
import time
from flock import Flock
import sys

def main():
    pygame.init()
    display = pygame.display.set_mode((700, 600))
    random.seed(time.time())

    flock = Flock(50)
    clock = pygame.time.Clock()

    useTree = True
    showTree = True
    useCohesion = True
    useSeperation = True
    useAlignment = True

    instructions = """
    Click Mouse to add Boid.
    Press 1 to toggle use Quad-tree.
    Press 2 to toggle show Quad-tree.
    Press 3 to toggle Cohesion between Boids.
    Press 4 to toggle Seperation between Boids.
    Press 5 to toggle Alignment between Boids.
    """
    print(instructions)


    while True:

        clock.tick(30)
        fps = clock.get_fps()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                flock.insertBoid((pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    #toggle using Quadtree
                    useTree = not useTree
                if event.key == pygame.K_2:
                    #toggle showing tree
                    showTree = not showTree
                if event.key == pygame.K_3:
                    #toggle Cohesion
                    useCohesion = not useCohesion
                if event.key == pygame.K_4:
                    #toggle Seperation
                    useSeperation = not useSeperation
                if event.key == pygame.K_5:
                    #toggle Alignment
                    useAlignment = not useAlignment
                if event.key == pygame.K_BACKSPACE:
                    flock.removeBoid()


        flockLen = len(flock.flock)
        pygame.display.set_caption("Boids Simulation - Boids: {0} - FPS: {1}".format(flockLen, int(fps)))

        states = '\r    # of Boids: {0},' \
                 ' Use Quad-tree: {1},' \
                 ' Show Quad-tree boundaries: {2},' \
                 ' Cohesion: {3},' \
                 ' Seperation: {4},' \
                 ' Alignment: {5}     '.\
            format(flockLen, useTree, showTree, useCohesion, useSeperation, useAlignment)

        print(states, end="")

        display.fill((10, 10, 60))
        flock.draw(useTree, showTree, useCohesion, useSeperation, useAlignment)
        pygame.display.flip()
main()
