import pygame
import random

class Point:
    def __init__(self, x, y, data = None):
        self.x = x
        self.y = y
        self.data = data

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (
            point.x >= self.x and
            point.x < self.x + self.w and
            point.y >= self.y and
            point.y < self.y + self.h
        )
    def getRect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)




class Quadtree:
    def __init__(self, rectBoundary, capacity = 4):

        if capacity >= 1 and type(capacity) == int:
            self.capacity = capacity
        else:
            self.capacity = 4

        self.rectBoundary = rectBoundary
        self.points = []
        self.isSubDivided = False

    def subdivide(self):
        #subdivide the space into 4 quadrants:
        #topRight, topLeft, botRight, botLeft
        x = self.rectBoundary.x
        y = self.rectBoundary.y
        w = self.rectBoundary.w
        h = self.rectBoundary.h

        topLeftRect = Rectangle(x, y, w/2, h/2)
        self.topLeft = Quadtree(topLeftRect, self.capacity)

        topRightRect = Rectangle(x + w/2, y, w/2, h/2)
        self.topRight = Quadtree(topRightRect, self.capacity)

        botLeftRect = Rectangle(x, y + h/2, w/2, h/2)
        self.botLeft = Quadtree(botLeftRect, self.capacity)

        botRightRect = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.botRight = Quadtree(botRightRect, self.capacity)

        self.isSubDivided = True

    def insert(self, point):

        if not self.rectBoundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.isSubDivided:
            self.subdivide()

        return (self.topLeft.insert(point) or
                self.topRight.insert(point) or
                self.botLeft.insert(point) or
                self.botRight.insert(point)
                )

    def drawBoundaries(self):

        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, (255, 255, 255), self.rectBoundary.getRect(), 1)

        if self.isSubDivided:
            if self.topLeft is not None:
                self.topLeft.drawBoundaries()
            if self.topRight is not None:
                self.topRight.drawBoundaries()
            if self.botLeft is not None:
                self.botLeft.drawBoundaries()
            if self.botRight is not None:
                self.botRight.drawBoundaries()




