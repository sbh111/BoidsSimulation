import pygame
import pygame.math as m
import random

class Boid:
    def __init__(self, pos = m.Vector2(0, 0), vel = m.Vector2(0, 0)):

        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        self.velocity = vel

        self.s = int(random.gauss(4,1))
        r = int(random.gauss(30, 20))
        self.neighborRadius =  r if self.s * 10 < r else self.s * 10
        self.maxSpeed = abs(random.gauss(6,1))

    def limitSpeed(self):
        r, phi = self.velocity.as_polar()

        if r > self.maxSpeed:
            self.velocity.from_polar((self.maxSpeed, phi))

    def wrapAround(self):
        x, y = self.pos
        w, h = pygame.display.get_surface().get_size()

        if x < 0:
            x = w
        elif x > w:
            x = 0

        if y < 0:
            y = h
        elif y > h:
            y = 0
        self.pos.update(x, y)


    def boundPos(self):
        x, y = self.pos
        w, h = pygame.display.get_surface().get_size()

        if x < 20:
            self.velocity += m.Vector2(5, 0)
        elif x > w - 20:
            self.velocity += m.Vector2(-5, 0)

        if y < 20:
            self.velocity += m.Vector2(0, 5)
        elif y > h - 20:
            self.velocity += m.Vector2(0, -5)



    def draw(self):
        screen = pygame.display.get_surface()
        x, y = self.pos
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), self.s)
        #pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), self.neighborRadius, 1)



    def update(self, acc):
        self.velocity += acc
        #self.boundPos()
        self.limitSpeed()
        self.pos += self.velocity
        self.wrapAround()





