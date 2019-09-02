import pygame
import random
import time
from quad_tree import *


def main():
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Test")
    random.seed(time.time())

    clock = pygame.time.Clock()

    pts = []
    qtree = Quadtree(Rectangle(0, 0, 601, 601), 1)
    for i in range(50):
        pts.append((random.randint(0, 600), random.randint(0, 600)))

    while True:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pts.append((pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN:
                if pygame.K_BACKSPACE and len(pts) > 0:
                    pts.pop()


        pts.append((random.randint(0, 600), random.randint(0, 600)))
        pts.pop(0)

        display.fill((0, 0, 50))
        #FIXME: python is not making a new Quadtree, its using the previous Quadtree object
        for pt in pts:
            pygame.draw.circle(display, (255, 0, 0), pt, 4)
            #qtree.insert(Point(pt[0], pt[1], pt))

        qtree.reset()
        qtree.insertPts(pts)
        qtree.drawBoundaries()
        pygame.display.flip()
main()