import pygame
import pygame.math as m

class Boid:
    def __init__(self, pos = m.Vector2(0, 0), vel = m.Vector2(1, 1), s = 1):

        self.pos = pos
        self.velocity = vel
        self.s = s

        self.neighborRadius = 50
        self.maxForce = 0.03
        self.maxSpeed = 3

    def getPos(self):
        return self.pos

    def getNeighborRadius(self):
        return self.neighborRadius

    def draw(self):
        screen = pygame.display.get_surface()
        x, y = self.pos
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), self.s)
        #pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), self.neighborRadius, 1)



    def update(self, acc):
        self.velocity += acc
        self.limitSpeed()
        self.pos += self.velocity
        self.wrapAround()

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



