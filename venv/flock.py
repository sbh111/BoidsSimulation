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
            vel = m.Vector2(random.randrange(-2, 2), random.randrange(-2, 2))

            flockList.append(Boid(m.Vector2(x, y), vel, 5))
        return flockList


    def cohesion(self, myBoid, neighbors):
        #Rule 1: Boids try to fly towards the centre of mass of neighbouring boids.

        if len(neighbors) == 0:
            return m.Vector2(0, 0)

        centerOfPos = m.Vector2(0, 0)

        for neighbor in neighbors:
            centerOfPos += neighbor.getPos()

        centerOfPos /= len(neighbors)
        acc = centerOfPos - myBoid.getPos()
        return acc

    def seperation(self, myBoid, neighbors):
        #Rule 2: Boids try to keep a small distance away from other objects (including other boids).
        if len(neighbors) == 0:
            return m.Vector2(0, 0)

        acc = m.Vector2(0, 0)
        for neighbor in neighbors:
            if (myBoid.getPos().distance_to(neighbor.getPos()) < myBoid.getNeighborRadius()) and (neighbor is not myBoid):
                v = (myBoid.getPos() - neighbor.getPos())
                r, phi = v.as_polar()
                r = r**-1
                v.from_polar((r, phi))
                acc += v
        return acc


    def intersects(self, myBoid):
        neighbors = []
        for boid in self.flock:
            if (myBoid.getPos().distance_to(boid.getPos()) <= myBoid.getNeighborRadius()) and (boid is not myBoid):
                neighbors.append(boid)
        return neighbors

    def draw(self):
        for boid in self.flock:
            neighbors = self.intersects(boid)

            acc = m.Vector2(0, 0)
            acc += (.01 * self.cohesion(boid, neighbors))
            acc += (self.seperation(boid, neighbors))

            boid.update(acc)
            boid.draw()
