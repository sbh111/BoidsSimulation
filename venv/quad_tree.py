import pygame
import queue
from shapes import *


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

    def query(self, range, isIterative = False):
        dataList = []
        if isIterative:
            iterativeQuery(self.root, dataList, range)
        else:
            recursiveQuery(self.root, dataList, range)
        return [pt.data for pt in dataList]

    def drawBoundaries(self):
        screen = pygame.display.get_surface()
        recursiveDrawBoundaries(self.root, screen)

    def reset(self):
        self.root.points = []
        self.root.children = []
        self.root.isSubdivided = False



#Quadtree helpers

def recursiveQuery(node, dataList, range):
    if not node.rectBoundary.intersects(range):
        return
    elif node.isSubdivided:
        for child in node.children:
            if child.rectBoundary.intersects(range):
                recursiveQuery(child, dataList, range)
        return

    #now have reached a leaf, where the point data is stored
    pts = range.containsPts(node.points)
    dataList.extend(pts)
    return


def iterativeQuery(root, dataList, range):
    stack = queue.LifoQueue()
    stack.put(root)

    while not stack.empty():
        node = stack.get()

        if not node.rectBoundary.intersects(range):
            continue
        elif node.isSubdivided:
            for child in node.children:
                stack.put(child)
        else:
            #range intersects the boundary, and the node has not been subdivided
            #so need to test the points in the node to see if they are within range
            pts = range.containsPts(node.points)
            dataList.extend(pts)
    return






def recursiveDrawBoundaries(node, screen):
    pygame.draw.rect(screen, (120, 120, 120), node.rectBoundary.getRect(), 1)
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






