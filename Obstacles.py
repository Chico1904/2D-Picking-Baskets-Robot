"""
Created on Sat Apr 30 01:10:23 2022

@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with four classes, each one corresponds to a type of obstacle
"""
from graphics import *
from random import *


class Tree:
    """
    A class that creates a tree in the graphical window
    """

    def __init__(self, p1, p2):
        """
        :param p1 and p2: corners of the rectangle that surrounds the entire tree
        """

        self.p1 = Point(min(p1.getX(), p2.getX()), min(p1.getY(), p2.getY()))
        self.p2 = Point(max(p1.getX(), p2.getX()), max(p1.getY(), p2.getY()))
        self.width = abs(self.p2.getX() - self.p1.getX())
        self.height = abs(self.p2.getY() - self.p1.getY())
        self.radius = min(self.width / 2, self.height / 2)
        self.center = Point((self.p2.getX() + self.p1.getX()) / 2, (self.p2.getY() + self.p1.getY()) / 2)

    def draw(self, win):
        """
        function that defines what the tree looks like in the graphics window
        :param win: graphics window
        """
        p3 = Point(self.p1.getX() + self.width / 4, self.p1.getY())  # canto inf. esq. do tronco
        p4 = Point(self.p2.getX() - self.width / 4, self.p2.getY() - self.radius)  # canto sup. dir. do tronco
        trunk = Rectangle(p3, p4)
        trunk.setFill('brown')

        p5 = Point(self.center.getX(), self.p2.getY() - self.radius)  # centro das folhas da arvore
        leaves = Circle(p5, self.radius)
        leaves.setFill('green')

        trunk.draw(win)
        leaves.draw(win)

    def zone(self, particle, robot_width, robot_height):
        """
        function that will evaluate, at each position update, if there is a collision.
        when the zone is false, there is collision
        :param particle: particle that coincides with the robot's center
        :param robot_width: robot's width
        :param robot_height: robot's height
        """
        zone_tree = True
        if (abs(particle.getX() - self.center.getX()) - (robot_width / 2 + self.radius)) <= 0.1 and \
                (abs(particle.getY() - self.center.getY()) - (robot_height / 2 + self.height / 2)) <= 0.1:
            zone_tree = False
        else:
            zone_tree = True
        return zone_tree

    def getWidth(self):
        # Function that returns the value of the tree's width
        return self.width

    def getHeight(self):
        # Function that returns the value of the tree's height
        return self.height

    def getCenter(self):
        # Function that returns the value of the tree's center
        return self.center


class Stone:
    """
    A class that creates a stone in the graphical window
    """

    def __init__(self, center, radius):
        """
        :param center: center of the circle that defines the stone
        :param radius: radius of the circle that defines the stone
        """
        self.center = center
        self.radius = radius

    def draw(self, win):
        """
        function that defines what the stone looks like in the graphics window
        :param win: graphics window
        """
        stone = Circle(self.center, self.radius)
        stone.draw(win)
        stone.setFill('grey')

    def zone(self, particle, robot_width, robot_height):
        """
        function that will evaluate, at each position update, if there is a collision.
        when the zone is false, there is collision
        :param particle: particle that coincides with the robot's center
        :param robot_width: robot's width
        :param robot_height: robot's height
        """
        zone_stone = True
        if (abs(particle.getX() - self.center.getX()) - (robot_width / 2 + self.radius) <= 0.1) and \
                (abs(particle.getY() - self.center.getY()) - (robot_height / 2 + self.radius) <= 0.1):
            zone_stone = False
        else:
            zone_stone = True
        return zone_stone

    def getCenter(self):
        # Function that returns the value of the stone's center
        return self.center

    def getWidth(self):
        # Function that returns the value of the stone's width
        return 2 * self.radius

    def getHeight(self):
        # Function that returns the value of the stone's height
        return 2 * self.radius


class Grass:
    """
    A class which creates grass in the graphical window
    """

    def __init__(self, p1, p2):
        """
        :param p1 and p2: corners of the rectangle that surrounds the entire grass
        """
        self.p1 = Point(min(p1.getX(),p2.getX()), min(p1.getY(),p2.getY()))
        self.p2 = Point(max(p1.getX(),p2.getX()), max(p1.getY(),p2.getY()))
        self.width = abs((self.p1.getX() - self.p2.getX()))
        self.height = abs((self.p1.getY() - self.p2.getY()))
        self.p3 = Point(self.p2.getX(), self.p2.getY() - self.height * (1 / 2))
        self.center = Point((self.p1.getX() + self.p2.getX()) / 2, (self.p1.getY() + self.p2.getY()) / 2)

    def draw(self, win):
        """
        function that defines what the grass looks like in the graphics window
        :param win: graphics window
        """
        grass = Rectangle(self.p1, self.p3)
        grass.draw(win)
        grass.setFill('green')

        # to simulate the grass, we use the random function to generate the bits of grass (with a rectangular shape)
        points = [self.p1.getX(), self.p2.getX()]
        points.sort()
        cont = points[0]
        while cont < points[1]:
            # we will draw rectangles with random height and with a width = 0.5 across the width of the grass
            h = self.height * (1 / 2) * random()
            p4 = Point(cont, self.p3.getY())
            cont += 0.5
            p5 = Point(cont, self.p3.getY() + h)
            rectangle = Rectangle(p4, p5)
            rectangle.setFill('green')
            rectangle.draw(win)

    def zone(self, particle, robot_width, robot_height):
        """
        function that will evaluate, at each position update, if there is a collision.
        when the zone is false, there is collision
        :param particle: particle that coincides with the robot's center
        :param robot_width: robot's width
        :param robot_height: robot's height
        """
        zone_grass = True
        if abs(particle.getX() - self.center.getX()) - (robot_width / 2 + self.width / 2) <= 0.05 and \
                abs(particle.getY() - self.center.getY()) - (robot_height / 2 + self.height / 2) <= 0.05:
            zone_grass = False
        else:
            zone_grass = True
        return zone_grass

    def getCenter(self):
        # Function that returns the value of the grass' center
        return self.center

    def getWidth(self):
        # Function that returns the value of the grass' width
        return self.width

    def getHeight(self):
        # Function that returns the value of the grass' height
        return self.height


class Bush:
    """
    A class which creates a bush in the graphical window
    """

    def __init__(self, p1, p2):
        """
        :param p1 and p2: corners of the rectangle that surrounds the entire bush
        """
        self.p1 = p1
        self.p2 = p2
        self.width = abs(self.p1.getX() - self.p2.getX())
        self.height = abs(self.p1.getY() - self.p2.getY())
        self.center = Point((self.p1.getX() + self.p2.getX()) / 2, (self.p1.getY() + self.p2.getY()) / 2)

    def draw(self, win):
        """
        function that defines what the bush looks like in the graphics window
        :param win: graphics window
        """
        bush = Oval(self.p1, self.p2)
        bush.draw(win)
        bush.setFill('green')

    def zone(self, particle, robot_width, robot_height):
        """
        function that will evaluate, at each position update, if there is a collision.
        when the zone is false, there is collision
        :param particle: particle that coincides with the robot's center
        :param robot_width: robot's width
        :param robot_height: robot's height
        """
        zone_bush = True
        if (abs(particle.getX() - self.center.getX()) - (robot_width / 2 + self.width / 2) <= 0.1) and \
                (abs(particle.getY() - self.center.getY()) - (robot_height / 2 + self.height / 2) <= 0.1):
            zone_bush = False
        else:
            zone_bush = True
        return zone_bush

    def getCenter(self):
        # Function that returns the value of the bush's center
        return self.center

    def getWidth(self):
        # Function that returns the value of the bush's width
        return self.width

    def getHeight(self):
        # Function that returns the value of the bush's height
        return self.height
