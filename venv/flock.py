import pygame
import pygame.math as m
import random
from boid import Boid
from quad_tree import *

class Flock:
    def __init__(self, popSize):
        self.flock = self.createFlock(popSize)

        w, h = pygame.display.get_surface().get_size()
        boundary = Rectangle(0, 0, w + 1, h + 1)
        self.quadtree = Quadtree(boundary, 8)


    def createFlock(self, popSize):
        flockList = []
        for i in range(popSize):
            x, y = pygame.display.get_surface().get_size()
            x = random.randint(0, x)
            y = random.randint(0, y)
            vel = m.Vector2(random.uniform(-10, 10), random.uniform(-10, 10))

            flockList.append(Boid(m.Vector2(x, y), vel))
        return flockList


    '''=================The Rules for Flocking======================='''

    def cohesion(self, myBoid, neighbors):
        #Rule 1: Boids try to fly towards the centre of mass of neighbouring boids.
        if len(neighbors) == 0:
            return m.Vector2(0, 0)

        centerOfPos = m.Vector2(0, 0)

        for neighbor in neighbors:
            centerOfPos += neighbor.pos

        centerOfPos /= len(neighbors)
        acc = centerOfPos - myBoid.pos
        return acc

    def seperation(self, myBoid, neighbors):
        #Rule 2: Boids try to keep a small distance away from other objects (including other boids).
        if len(neighbors) == 0:
            return m.Vector2(0, 0)

        acc = m.Vector2(0, 0)
        for neighbor in neighbors:
            if myBoid.pos.distance_to(neighbor.pos) < myBoid.neighborRadius:
                v = (myBoid.pos - neighbor.pos)
                r, phi = v.as_polar()
                if r > 0:
                    r = r**-1
                v.from_polar((r, phi))
                acc += v
        return acc

    def alignment(self, myBoid, neighbors):
        #Rule 3: Boids try to match velocity with nearby boids.
        if len(neighbors) == 0:
            return m.Vector2(0, 0)

        v = m.Vector2(0, 0)
        for neighbor in neighbors:
            v += neighbor.velocity
        v /= len(neighbors)
        acc = v - myBoid.velocity
        return acc


    def inNeighboorhood(self, myBoid, useQtree):
        neighbors = []

        if useQtree:
            #O(nLog(n))) algorithm for finding boids in radius
            circleRange = Circle(myBoid.x, myBoid.y, myBoid.neighborRadius)
            neighbors.extend(self.quadtree.query(circleRange))
        else:
            #O(n^2) algorithm for finding boids in radius
            for boid in self.flock:
                if (myBoid.pos.distance_to(boid.pos) <= myBoid.neighborRadius) and (boid is not myBoid):
                    neighbors.append(boid)

        return neighbors



    def draw(self, useQtree = True, showQtree = True):


        self.quadtree.reset()
        self.quadtree.insertPts(self.flock)


        for boid in self.flock:
            neighbors = self.inNeighboorhood(boid, useQtree)

            acc = m.Vector2(0, 0)
            acc += (.005 * self.cohesion(boid, neighbors))
            acc += (1.1 * self.seperation(boid, neighbors))
            acc += (.3 * self.alignment(boid, neighbors))
            acc *= (1)
            if acc == m.Vector2(0, 0):
                acc += (.4 * m.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)))

            boid.update(acc)
            boid.draw()

        if showQtree:
            #boids have updated, so remake the qtree
            self.quadtree.reset()
            self.quadtree.insertPts(self.flock)
            self.quadtree.drawBoundaries()


