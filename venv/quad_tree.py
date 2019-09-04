import pygame

class Point:
    def __init__(self, x, y, data = None):
        self.x = x
        self.y = y
        self.data = data


class Rectangle:
    def __init__(self, x, y, w, h):
        #x and y are coords for top left
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, boundary):
        if type(range) == type(Rectangle):

            #boundary's left, right, top, bottom
            l1 = boundary.x
            r1 = l1 + boundary.w
            t1 = boundary.y
            b1 = t1 + boundary.h

            #this rects left, right, top, bottom
            l0 = self.x
            r0 = l1 + self.w
            t0 = self.y
            b0 = t1 + self.h

            return not (r0 < l1 or r1 < l0 or
                        t0 > b1 or t1 > b0
                        )

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

    def drawBoundaries(self):
        screen = pygame.display.get_surface()
        recursiveDrawBoundaries(self.root, screen)

    def reset(self):
        self.root.points = []
        self.root.children = []
        self.root.isSubdivided = False



#Quadtree helpers
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






