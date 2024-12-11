"""
Created on Fri Apr 29 10:59:24 2022

@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with the Basket class
"""
from graphics import *


class Basket:
    """
    A class which creates a basket in the graphical window
    """

    def __init__(self, radius, color, center):
        """
        :param center: center of the circle that defines the basket
        :param radius: radius of the circle that defines the basket
        :param color: colour of the basket
        """
        self.radius = radius
        self.color = color
        self.center = center
        self.circle = Circle(self.center, self.radius)
        self.circle.setFill(self.color)
        self.fruit_1 = Circle(self.center, self.radius / 3)
        self.fruit_1.setFill('red')
        p2 = Point(self.center.getX() + self.radius / 3, self.center.getY() + self.radius / 3)
        self.fruit_2 = Circle(p2, self.radius / 3)
        self.fruit_2.setFill('yellow')
        p3 = Point(self.center.getX() - self.radius / 3, self.center.getY() + self.radius / 3)
        self.fruit_3 = Circle(p3, self.radius / 3)
        self.fruit_3.setFill('green')

    def draw(self, win):
        """
        function that defines what the basket looks like in the graphics window
        :param win: graphics window
        """
        self.circle.draw(win)
        self.fruit_1.draw(win)
        self.fruit_2.draw(win)
        self.fruit_3.draw(win)

    def undraw(self):
        # function that undraws the existing basket so a new one can be drawn in the next frame
        self.circle.undraw()
        self.fruit_1.undraw()
        self.fruit_2.undraw()
        self.fruit_3.undraw()

    def move(self, dx, dy):
        # function that moves the basket
        self.circle.move(dx, dy)
        self.fruit_1.move(dx, dy)
        self.fruit_2.move(dx, dy)
        self.fruit_3.move(dx, dy)




