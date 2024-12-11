# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:59:24 2022
 @author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with the Button class
"""
from graphics import *


class Button:
    """ A class that creates buttons to interact with the program """

    def __init__(self, win, height, width, center, message, color):
        """
        :param win: graphics window
        :param height: button's height
        :param width: button's width
        :param center: button's center
        :param message: message in the button
        """
        self.win = win
        self.height, self.width, self.center = height, width, center
        self.message = message
        self.label = message
        self.p1 = Point(self.center.getX() - width/2, self.center.getY() - height/2)
        self.p2 = Point(self.center.getX() + width/2, self.center.getY() + height/2 )
        self.rectangle = Rectangle(self.p1, self.p2)
        self.rectangle.setFill(color)

        self.message = Text(center, message)
        self.rectangle.draw(win)
        self.message.draw(win)

    def clicked(self, p):
        """
        Function that evaluates if the button was clicked
        :param p: point clicked by the user
        """
        if (self.p1.getX() <= p.getX() <= self.p2.getX()) and (self.p1.getY() <= p.getY() <= self.p2.getY()):
            return True
        else:
            return False

