"""
Created on Fri Apr 29 11:45:00 2022
@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with the Particle class
"""

from math import sqrt


class Particle:
    """
    class that allows reducing the robot to a particle. Robot motion will be defined at the expense of particle motion
    """

    def __init__(self, initial_point, velocity):
        """
        :param initial_point:  which will  coincide with the particle
        :param velocity: body speed
        """
        self.initial_point = initial_point
        self.vel = velocity
        self.xpos = self.initial_point.getX()
        self.ypos = self.initial_point.getY()

    def getY(self):
        # Returns the y position of the particle
        return self.ypos

    def getX(self):
        # Returns the x position of the particle
        return self.xpos

    def new_position(self, input_point, dt):
        """
        Function that updates the position of the particle according to the input_point
        :param input_point: point given by the user (i.p)
        :param dt: Time interval separating each update
        :return:distance traveled in each update
        """
        # we need the previous update position to determine the travelled distance
        latest_xpos = self.xpos
        latest_ypos = self.ypos

        dx = input_point.getX() - self.xpos  # dx is the x distance between the actual particle position and the i.p
        dy = input_point.getY() - self.ypos  # dy is the y distance between the actual particle position and the i.p
        d = sqrt(dx ** 2 + dy ** 2)

        try:
            # we divided the velocity into two components, so that the robot moved diagonally
            vel_x = self.vel * (dx / d)
            vel_y = self.vel * (dy / d)
            self.xpos += vel_x * dt
            self.ypos += vel_y * dt

            d_travelled = sqrt((self.xpos - latest_xpos) ** 2 + (self.ypos - latest_ypos) ** 2)

            return d_travelled
        except:
            # If the user clicks on the robot without having clicked on an input point before,
            # d=0 and there would be an error. This structure serves to avoid division by 0
            d_travelled = 0
            return d_travelled

    def moveX(self, dt, acum_x, x_signal):
        """
        Function that moves the particle horizontally. This is necessary in the deviation movement
        :param dt: Time interval separating each update
        :param acum_x: x distance traveled until the current update, increases with each update
        :param x_signal: indicates the sense of the velocity
        :return: acum_x (total x distance traveled ) and d_travelled (x distance traveled in one update)
        """
        vel = x_signal * self.vel
        preview_xpos = self.xpos
        self.xpos += vel * dt
        acum_x += self.xpos - preview_xpos
        d_travelled = abs(self.xpos - preview_xpos)

        return acum_x, d_travelled

    def moveY(self, dt, acum_y, y_signal):
        """
        Function that moves the particle vertically. This is necessary in the deviation movement
        :param dt: Time interval separating each update
        :param acum_y: y distance traveled until the current update, increases with each update!
        :param y_signal: indicates the sense of the velocity
        :return: acum_y (total y distance traveled ) and d_travelled (y distance traveled in one update)
        """
        vel = y_signal * self.vel
        preview_ypos = self.ypos
        self.ypos += vel * dt
        acum_y += self.ypos - preview_ypos
        d_travelled = abs(self.ypos - preview_ypos)

        return acum_y, d_travelled
