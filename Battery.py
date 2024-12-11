"""
Created on Wed May 25 09:10:23 2022

@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with the Battery class
"""
from graphics import *


class Battery:
    """ class that creates the harvey's battery and controls its energy """

    def __init__(self, width, height, center, win):
        self.width = width
        self.height = height
        self.center = center
        self.p1 = Point(center.getX() - self.width / 2, center.getY() - self.height / 2)
        self.p2 = Point(center.getX() + self.width / 2, center.getY() + self.height / 2)
        self.body = Rectangle(self.p1, self.p2)
        self.body.draw(win)
        self.initial_charge = 800
        self.charge = self.initial_charge
        colors = ['red', 'orange', 'yellow', 'green']
        self.rectangles = []
        for cont in range(4):
            p3 = Point(self.p1.getX() + cont * (self.width / 4), self.p1.getY())
            p4 = Point(self.p1.getX() + (cont + 1) * (self.width / 4), self.p2.getY())
            rectangle = Rectangle(p3, p4)
            rectangle.setFill(colors[cont])
            rectangle.draw(win)
            self.rectangles.append(rectangle)  # list with 4 rectangles, battery charge indicators

    def undraw(self):
        # function that erases the battery
        self.body.undraw()
        for cont in range(4):
            self.rectangles[cont].undraw()

    def getCharge(self):
        # Function that returns the value of the battery's charge
        return self.charge

    def updateCharge(self, d_travelled):
        # Function that updates the value of the battery's charge while travelling
        self.charge -= d_travelled

    def move(self, dx, dy):
        # function that moves the battery
        self.body.move(dx, dy)
        for cont in range(4):
            self.rectangles[cont].move(dx, dy)

    def chargeBattery(self, win):
        #  Function that updates the battery's charge value and battery's draw while charging
        self.rectangles[0].undraw()
        for cont in range(4):
            try:
                self.rectangles[cont].draw(win)
            except:
                continue
        self.charge = self.initial_charge

    def updateChargeColor(self):
        # Function that updates the battery's draw's active colors to make the user know what's the battery charge
        color = ''
        if 0.5 * self.initial_charge < self.charge <= 0.75 * self.initial_charge:
            self.rectangles[3].undraw()  # delete the green rectangle
        elif 0.25 * self.initial_charge < self.charge <= 0.5 * self.initial_charge:
            self.rectangles[2].undraw()  # delete the yellow rectangle
        elif self.charge <= 0.25 * self.initial_charge:
            self.rectangles[1].undraw()  # delete the orange rectangle
            color = 'red'
        return color
