import pygame
import pygame.math as m

class Boid:
    def __init__(self, pos = m.Vector2(0, 0), vel = m.Vector2(1, 1), s = 1):

        self.pos = pos
        self.velocity = vel
        self.s = s

        self.radius = 5
        self.maxForce = 0.03
        self.maxSpeed = 2

    def draw(self):
        screen = pygame.display.get_surface()
        x, y = self.pos
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), self.s)


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



