import pygame
import math

class Point:
    def __init__(self, x, y, data = None):
        self.x = x
        self.y = y
        self.data = data

    @staticmethod
    def distToLine(px, py, lx1, ly1, lx2, ly2):
        A = px - lx1
        B = py - ly1
        C = lx2 -lx1
        D = ly2 - ly1

        dot = A * C + B * D
        lenSq = C**2 + D**2
        param = -1

        if not lenSq == 0:
            param = dot / lenSq

        if param < 0:
            xx = lx1
            yy = ly1
        elif param > 1:
            xx = lx2
            yy = ly2
        else:
            xx = lx1 + param * C
            yy = ly1 + param * D

        dx = px - xx
        dy = py - yy

        return math.sqrt(dx**2 + dy**2)


class Circle:
    def __init__(self, x, y, r):
        self.radius = r
        self.x = x
        self.y = y

    def containsPts(self, points):
        containsPts = []
        for pt in points:
            dist = (self.x - pt.x)**2 + (self.y - pt.y)**2
            dist = math.sqrt(dist)
            if dist < self.radius:
                containsPts.append(pt)
        return containsPts

    def containsPt(self, point):
        dist = (self.x - point.x) ** 2 + (self.y - point.y) ** 2
        dist = math.sqrt(dist)
        return dist < self.radius





class Rectangle:
    def __init__(self, x, y, w, h):
        #x and y are coords for top left
        self.x = x
        self.y = y
        self.w = w
        self.h = h


    def intersects(self, boundary):
        # this rects left, right, top, bottom
        l0 = self.x
        r0 = l0 + self.w
        t0 = self.y
        b0 = t0 + self.h

        if type(boundary) == Rectangle:
            #boundary's left, right, top, bottom
            l1 = boundary.x
            r1 = l1 + boundary.w
            t1 = boundary.y
            b1 = t1 + boundary.h

            return not (r0 < l1 or r1 < l0 or
                        t0 > b1 or t1 > b0
                        )

        if type(boundary) == Circle:
            cx = boundary.x
            cy = boundary.y
            cr = boundary.radius

            if self.containsPt(Point(cx, cy)):
                return True

            if(
                Point.distToLine(cx, cy, l0, t0, l0, b0) <= cr or #check left line intersection
                Point.distToLine(cx, cy, r0, t0, r0, b0) <= cr or #check right
                Point.distToLine(cx, cy, l0, t0, r0, t0) <= cr or #check top
                Point.distToLine(cx, cy, l0, b0, r0, b0) <= cr    #check bottom
            ):
                return True

            #else no intersection
            return False
        raise Exception("boundary should be a Rectangle or Circle type")


    def containsPts(self, points):
        containsPts = []
        for pt in points:
            if(
            pt.x >= self.x and
            pt.x < self.x + self.w and
            pt.y >= self.y and
            pt.y < self.y + self.h):
                containsPts.append(pt)
        return containsPts

    def containsPt(self, point):
        return (
                point.x >= self.x and
                point.x < self.x + self.w and
                point.y >= self.y and
                point.y < self.y + self.h
        )

    def getRect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))







class Node:
    def __init__(self, rectBoundary, points = []):
        self.rectBoundary = rectBoundary
        self.points = points
        self.children = []
        self.isSubdivided = False





class Quadtree:
    def __init__(self, rectBoundary, capacity = 4):
        self.root = Node(rectBoundary)
        self.capacity = capacity

    def subdivide(self):
        recursiveSubdivide(self.root, self.capacity)

    def insert(self, point):
        recursiveInsert(self.root, self.capacity, point)

    def insertPts(self, objects):
        for object in objects:
            if not type(object) == type(Point):
                if type(object) == tuple:
                    recursiveInsert(self.root, self.capacity, Point(object[0], object[1], object))
                else:
                    recursiveInsert(self.root, self.capacity, Point(object.x, object.y, object))
            else:
                recursiveInsert(self.root, self.capacity, point)

    def query(self, range):
        pts = []
        recursiveQuery(self.root, pts, range)
        return pts

    def drawBoundaries(self):
        screen = pygame.display.get_surface()
        recursiveDrawBoundaries(self.root, screen)

    def reset(self):
        self.root.points = []
        self.root.children = []
        self.root.isSubdivided = False



#Quadtree helpers

def recursiveQuery(node, pts, range):
    if not node.rectBoundary.intersects(range):
        return
    elif node.isSubdivided:
        for child in node.children:
            recursiveQuery(child, pts, range)

    #now have reached a leaf, where the point data is stored
    containsPts = range.containsPts(node.points)
    pts.extend(containsPts)
    return




def recursiveDrawBoundaries(node, screen):
    pygame.draw.rect(screen, (100, 100, 100), node.rectBoundary.getRect(), 1)
    if len(node.children) > 0:
        for child in node.children:
            recursiveDrawBoundaries(child, screen)
    return


def recursiveInsert(node, capacity, point):
    if not node.rectBoundary.containsPt(point):
        return False

    #else boundary contains point

    if (not node.isSubdivided) and (len(node.points) <= capacity):
        node.points.append(point)
        recursiveSubdivide(node, capacity)
        return True

    if(node.isSubdivided):
        r = False
        for child in node.children:
            r = r or recursiveInsert(child, capacity, point)
        return r


def recursiveSubdivide(node, capacity):
    if len(node.points) <= capacity:
        return

    #else redistribute points to new 4 quadrants
    newW = node.rectBoundary.w / 2
    newH = node.rectBoundary.h / 2
    x = node.rectBoundary.x
    y = node.rectBoundary.y

    topLeftRect = Rectangle(x, y, newW, newH)
    pts = topLeftRect.containsPts(node.points)
    topLeft = Node(topLeftRect, pts)
    recursiveSubdivide(topLeft, capacity)

    topRightRect = Rectangle(x + newW, y, newW, newH)
    pts = topRightRect.containsPts(node.points)
    topRight = Node(topRightRect, pts)
    recursiveSubdivide(topRight, capacity)

    botLeftRect = Rectangle(x, y + newH, newW, newH)
    pts = botLeftRect.containsPts(node.points)
    botLeft = Node(botLeftRect, pts)
    recursiveSubdivide(botLeft, capacity)

    botRightRect = Rectangle(x + newW, y + newH, newW, newH)
    pts = botRightRect.containsPts(node.points)
    botRight = Node(botRightRect, pts)
    recursiveSubdivide(botRight, capacity)

    node.children = [topLeft, topRight, botLeft, botRight]
    node.points = []
    node.isSubdivided = True
    return






