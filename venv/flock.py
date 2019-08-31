import pygame
import pygame.math as m
import time
import random
from boid import Boid

class Flock:
    def __init__(self, population):
        self.flock = self.createFlock(population)
        random.seed(time.time())

    def createFlock(self, population):
        flockList = []
        for i in range(population):
            x, y = pygame.display.get_surface().get_size()
            x = random.randint(0, x)
            y = random.randint(0, y)
            vel = m.Vector2(random.random()*2 - 1, random.random()*2 - 1)

            flockList.append(Boid(m.Vector2(x, y), vel, 5))
        return flockList

    def draw(self):
        for boid in self.flock:
            acc =  m.Vector2(random.random()*2 - 1, random.random()*2 - 1)
            boid.update(acc)
            boid.draw()
