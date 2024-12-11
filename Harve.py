"""
Created on Sat Apr 30 01:10:23 2022

@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with the Harve class (robot)
"""
from Particle import *
from Basket import *
from Battery import *


class Harve:
    """
    Class that defines the robot, the elements that allow it to be coupled (basket and battery) and the methods that
     allow to control the robot (its movement and the interconnection with the basket and the battery)
    """

    def __init__(self, win, radius, initial_point, main_color, velocity):
        self.win = win
        self.radius = radius
        self.initial_point = initial_point

        # the next 2 attributes allow defining the robot's zone
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.main_color = main_color

        # We define the particle as the center of the robot
        # It is from it that we define the movement of the same
        self.particle = Particle(self.initial_point, velocity)

        # Now we define the robot's body plus the basket, which will only be drawn after it has been collected
        self.body = Circle(self.initial_point, self.radius)
        self.body.setFill(main_color)
        self.body.draw(win)

        self.cesto_robot = Basket(2, 'orange', initial_point)

        # We define the battery at the expense of the robot's dimensions and couple it to the robot
        p1 = Point(self.initial_point.getX() - self.radius / 4, self.initial_point.getY() - (5 / 8) * self.radius)
        self.battery = Battery(self.radius / 2, self.radius / 4, p1, win)

    def getCenter(self):
        # Returns the center of the robot
        return Point(self.particle.getX(), self.particle.getY())

    def getWidth(self):
        # Returns the width of the robot
        return self.width

    def getHeight(self):
        # Returns the height of the robot
        return self.height

    def undraw(self):
        # Erases the robot body (circle) and its battery
        self.body.undraw()
        self.battery.undraw()

    def drawBasket(self, win):
        # If the basket is already drawn, it gives an error, so this structure is for, in case the basket is already
        # drawn, the function is not executed (uncommon error but it happened)
        try:
            self.cesto_robot.draw(win)
        except:
            pass

    def undrawBasket(self):
        # Function that deletes the basket that is attached to the robot
        self.cesto_robot.undraw()

    def undrawBattery(self):
        # Function that only erases the robot's battery
        self.battery.undraw()

    # -----------------------------------------IMPLEMENTATION 1-4 FUNCTIONS -------------------------------------------

    def updatePosition(self, destination, movement_type):
        """
        A function that will update the position of the robot, making the centre of the robot move with each update, in
        order to be coincident with the particle, which is what really defines the robot's movement

        :param destination : point given by user (i.p)
        :param movement_type: indicates whether the robot's movement is normal or contour. If it is not contour,
                                the particle update is made in this function. Otherwise, it is done in another
        :return: distance traveled in each update, which will only be necessary from the 2nd implementation,
         for the battery
        """
        # We invoke the method associated with the particle that updates its position taking into account the i.p
        # The first one will return the distance traveled between each update, which is necessary for the correct
        # battery operation

        d_travelled = 0  # we set the variable to be equal to zero so there are no assignment problems
        if movement_type != 'deviation':
            # If the movement is not contour, the particle update is made
            d_travelled = self.particle.new_position(destination, 1 / 100)

        center = self.body.getCenter()
        dx = self.particle.getX() - center.getX()
        dy = self.particle.getY() - center.getY()

        # We now move the robot (its body, battery and basket attached to it) to the new particle point
        self.body.move(dx, dy)

        self.battery.move(dx, dy)
        self.cesto_robot.move(dx, dy)

        return d_travelled

    def sideDeviationMovement(self, var_y, var_x, y_signal, x_signal, obstacle_center, obstacle_height, input_point):
        """
        Function responsible for the deflection movement when the obstacle collides with the lateral side. In this case,
        the robot  will have to make a vertical movement first and then a horizontal one. There, it will be able to
        go to its destination without colliding with the obstacle.

        :param var_x: gives us the distance in x that the robot has to travel to complete the contour
        :param var_y: gives us the distance in y that the robot has to travel to complete the contour
        :param x_signal: indicates whether the robot, just before the collision, was moving left or right
        :param y_signal: indicates whether the robot, just before the collision, was moving up or down
        :param obstacle_center: center point of the obstacle
        :param obstacle_height: obstacle height
        :param input_point: point given by the user
        """
        acum_y, acum_x = 0, 0

        while abs(var_y) + 0.1 >= abs(acum_y):
            # +0.1 is due to the existence of uncertainties during the calculation of the distance traveled. As long as
            # the robot doesn't travel the vertical distance necessary to avoid the robot, we update its position

            acum_y, d_travelled = self.particle.moveY(1 / 100, acum_y, y_signal)  # particle update
            self.updateBattery(d_travelled)
            self.updatePosition(None, 'deviation')  # robot update, that follows the particle

            if self.particle.getY() >= 100 - self.height / 2 or self.height / 2 >= self.particle.getY():
                # if the robot bumps into the window limits, changes the direction of movement
                y_signal = -y_signal
                var_y = ((obstacle_center.getY() + y_signal * obstacle_height / 2) + (y_signal * self.height / 2)) \
                        - self.particle.getY()  # vertical distance needed to avoid the robot
                acum_y = 0  # we have to reset the previously traveled distance
            update(100)

        if y_signal * input_point.getY() > y_signal * obstacle_center.getY() + obstacle_height / 2 + self.height / 2:
            # if only a contour movement is needed, the robot goes directly to the destination
            pass

        else:
            # if 2 contour movements are needed, we do the same now but horizontally
            while abs(var_x) + 0.1 >= abs(acum_x):
                acum_x, d_travelled = self.particle.moveX(1 / 100, acum_x, x_signal)
                self.updateBattery(d_travelled)
                self.updatePosition(None, 'deviation')
                update(100)

    def baseDeviationMovement(self, var_y, var_x, y_signal, x_signal, obstacle_center, obstacle_width, input_point):
        """
        Function responsible for the deflection movement when the obstacle collides with one of the bases. In this case,
        the robot  will have to make a horizontal movement first and then a vertical one. There, it will be able to
        go to its destination without colliding with the obstacle.

        :param var_x: gives us the distance in x that the robot has to travel to complete the contour
        :param var_y: gives us the distance in y that the robot has to travel to complete the contour
        :param x_signal: indicates whether the robot, just before the collision, was moving left or right
        :param y_signal: indicates whether the robot, just before the collision, was moving up or down
        :param obstacle_center: center point of the obstacle
        :param obstacle_width: obstacle width
        :param input_point: point given by the user
        """
        acum_y, acum_x = 0, 0

        while abs(var_x) + 0.1 >= abs(acum_x):
            # +0.1 is due to the existence of uncertainties during the calculation of the distance traveled. As long as
            # the robot doesn't travel the horizontal distance necessary to avoid the robot, we update its position

            acum_x, d_travelled = self.particle.moveX(1 / 100, acum_x, x_signal)  # particle update
            self.updateBattery(d_travelled)
            self.updatePosition(None, 'deviation')  # robot update, that follows the particle

            if self.particle.getX() >= 100 - self.width / 2 or self.width / 2 >= self.particle.getX():
                # if the robot bumps into the window limits, changes the direction of movement
                x_signal = -x_signal
                var_x = ((obstacle_center.getX() + x_signal * obstacle_width / 2) + (x_signal * self.width / 2)) \
                        - self.particle.getX()  # indica-nos se o robot estava a mover-se p/ esq ou p/ dir
                acum_x = 0  # we have to reset the previously traveled distance
            update(100)

        if x_signal * input_point.getX() > x_signal * obstacle_center.getX() + obstacle_width / 2 + self.width / 2:
            # if only a contour movement is needed, the robot goes directly to the destination
            pass

        else:
            # if 2 contour movements are needed, we do the same now but vertically
            while abs(var_y) + 0.1 >= abs(acum_y):
                acum_y, d_travelled = self.particle.moveY(1 / 100, acum_y, y_signal)
                self.updateBattery(d_travelled)
                self.updatePosition(None, 'deviation')
                update(100)

    def choosingDeviationMovement(self, collision_side, var_x, var_y, x_signal, y_signal, input_point, obstacle_height,
                                  obstacle_width, obstacle_center, obstacles, win, docstation_center, battery):
        """
        This function will determine the type of contour movement that the robot will make, depending on which side it
        collided with
        :param collision_side: side that collided with the obstacle, which could be the side or the base
        :param var_x: gives us the distance in x that the robot has to travel to complete the contour
        :param var_y: gives us the distance in y that the robot has to travel to complete the contour
        :param x_signal: indicates whether the robot, just before the collision, was moving left or right
        :param y_signal: indicates whether the robot, just before the collision, was moving up or down
        :param input_point: the point given by the user, the end point of the robot's movement
        :param obstacle_height: ""
        :param obstacle_width: ""
        :param obstacle_center: ""
        :param obstacles: list of obstacles in the graphics window
        :param win: graphics window
        :param docstation_center: center point of the docstation (robot charging station)
        :param battery: string that indicates if we want to the battery to be activated or not
        """
        if collision_side == 'lateral side':
            self.sideDeviationMovement(var_y, var_x, y_signal, x_signal, obstacle_center, obstacle_height, input_point)

        elif collision_side == 'base':
            self.baseDeviationMovement(var_y, var_x, y_signal, x_signal, obstacle_center, obstacle_width, input_point)

        self.movementMain(input_point, obstacles, win, docstation_center, battery)

    def movementAfterCollision(self, obstacle_width, obstacle_height, obstacle_center, input_point, dxx, dyy, win,
                               obstacles, docstation_center, battery):
        """
        We start by comparing the slopes of two "imaginary" lines:
          1- the straight line that passes through the center and a corner of the obstacle
          2- the straight line passing through the center of the robot and the center of the obstacle
         Comparing the module of the slopes, it's possible conclude if the robot collided by 1 of the bases or by
         the side. Then, we decide what the obstacle contour movement is, through the movement_decision function

        :param win: ""
        :param obstacles: list of obstacles
        :param obstacle_width: ""
        :param obstacle_height: ""
        :param obstacle_center: ""
        :param input_point: point given by the user
        :param dxx: last x variation of the robot, it indicates the sense of the deviation movement
                     ( to the right, dxx > 0, or to the left, dxx < 0)
        :param dyy:last y variation of the robot, it indicates the sense of the deviation movement
                     ( up, dyy > 0, or down, dyy < 0)
        :param docstation_center: center point of the docstation (robot charging station)
        :param battery: string that indicates if we want to the battery to be activated or not
        """
        slope_limit = (obstacle_height/2 + self.height/2) / (obstacle_width/2 + self.width/2)
        # limit slope that distinguishes a lateral collision from a base collision
        slope_robot_obstacle = (self.particle.getY() - obstacle_center.getY()) / (
                self.particle.getX() - obstacle_center.getX())  # slope between robot center and obstacle center
        if abs(slope_limit) >= abs(slope_robot_obstacle):
            lado = 'lateral side'
        else:
            lado = 'base'
        y_signal, x_signal = dyy / abs(dyy), dxx / abs(dxx)
        var_y = ((obstacle_center.getY() + y_signal * obstacle_height / 2) + (y_signal * self.height / 2)) \
                - self.particle.getY()  # distance in y that the robot has to travel to complete the contour
        var_x = ((obstacle_center.getX() + x_signal * obstacle_width / 2) + (x_signal * self.width / 2)) \
                - self.particle.getX()  # distance in x that the robot has to travel to complete the contour

        self.choosingDeviationMovement(lado, var_x, var_y, x_signal, y_signal, input_point, obstacle_height,
                                       obstacle_width, obstacle_center, obstacles, win, docstation_center, battery)

    def collisionEvaluation(self, obstacles, input_point, dxx, dyy, win, docstation_center, battery):
        """
        Function that evaluates if there is a collision with any obstacle and, if there is, gives its
         width/height/center and calls the function that will bypass the obstacle
        :param win: graphics window
        :param dyy: last y variation of the robot, it indicates the sense of the deviation movement
                     ( up, dyy > 0, or down, dyy < 0)
        :param dxx: last x variation of the robot, it indicates the sense of the deviation movement
                     ( to the right, dxx > 0, or to the left, dxx < 0)
        :param obstacles: lista de obstáculos
        :param input_point: point given by the user
        :param docstation_center: center point of the docstation (robot charging station)
        :param battery: string that indicates if we want to the battery to be activated or not
        """
        for cont in range(len(obstacles)):
            # to cd/ obstacle, see if the robot has entered the zone

            if not obstacles[cont].zone(self.particle, self.width, self.height):
                # if the robot enters the collision zone of 1 obstacle, we define an obstacle contour movement
                obstacle_width = obstacles[cont].getWidth()
                obstacle_height = obstacles[cont].getHeight()
                obstacle_center = obstacles[cont].getCenter()
                self.movementAfterCollision(obstacle_width, obstacle_height, obstacle_center, input_point, dxx, dyy,
                                            win, obstacles, docstation_center, battery)
                break

    def movementMain(self, destination, obstacles, win, docstation_center, battery):
        """
        Main robot movement function, which defines its movement in every implementation.
        Here, the robot's position is updated as long as its center is not (nearly) coincident with the entry point.
        In the 'while' loop, the function updates the robot's position, updates the battery (performing the move to
        recharge it if necessary) and make the obstacle avoidance movement if necessary.

         :param destination: end point of the movement, which can be the input point or the center of one of the docks
         :param obstacles: graphics window obstacle list
         :param win: graphical window
         :param docstation_center: center point of the docstation (robot charging station)
         :param battery: string that indicates if we want to the battery to be activated or not
        """
        dxx, dyy, latest_dxx, latest_dyy = 1, 1, 1, 1
        # these variables are defined here so there are no attribution errors
        # later, they will be used to define when the robot reaches its destination

        while (dxx * latest_dxx > 0) and (dyy * latest_dyy > 0):
            latest_dxx = destination.getX() - self.particle.getX()
            latest_dyy = destination.getY() - self.particle.getY()
            # we need to know the sign of the latest x/y displacement to define when did the robot reach the destination
            # Below, we take advantage of update_position function, which returns the distance traveled in each update
            d_travelled = self.updatePosition(destination, 'regular movement')
            update(100)

            if battery == 'battery activated':  # from the second implementation we want the battery to be functional
                color = self.updateBattery(d_travelled)  # charge value and battery color update
                if color == 'red':
                    self.chargeMovement(docstation_center, obstacles, win)
                    latest_dxx = destination.getX() - self.particle.getX()
                    latest_dyy = destination.getY() - self.particle.getY()
            # we need to know the sign of the new x/y displacement to define the obstacle contour movement
            dxx = destination.getX() - self.particle.getX()
            dyy = destination.getY() - self.particle.getY()

            # at each update, we'll see if there's collision with any obstacle and, in this case,do the contour movement
            self.collisionEvaluation(obstacles, destination, dxx, dyy, win, docstation_center, battery)

    # ----------------------------------------- IMPLEMENTATION 2-4 FUNCTIONS  ----------------------------------------

    def updateBattery(self, d_travelled):
        # Battery charge update, decreasing it with movement and updating its color, returning the latter
        self.battery.updateCharge(d_travelled)
        color = self.battery.updateChargeColor()

        return color

    def chargeMovement(self, docstation_center, obstacles, win):
        """
        Function that is called when the robot needs to charge the battery. Here, the robot heads to the center of the
         docstation, wait 1 second and update your battery indicator colors
        :param docstation_center: center point of the docstation (robot charging station)
        :param obstacles: list of obstacles
        :param win: graphics window
        """

        dxx, dyy, latest_dxx, latest_dyy = 1, 1, 1, 1
        # these variables are defined here so there are no attribution errors
        # later, they will be used to define when the robot reaches its destination
        while (dxx * latest_dxx > 0) and (dyy * latest_dyy > 0):
            latest_dxx = docstation_center.getX() - self.particle.getX()
            latest_dyy = docstation_center.getY() - self.particle.getY()
            self.updatePosition(docstation_center, 'regular movement')
            update(100)
            dxx = docstation_center.getX() - self.particle.getX()
            dyy = docstation_center.getY() - self.particle.getY()
            # we want to know the sign of the last dx/dy to define the obstacle contour movement

            self.collisionEvaluation(obstacles, docstation_center, dxx, dyy, win, docstation_center,
                                     'battery activated')
            # at each cycle/update, we will see if there is collision with any obstacle and, if there is
            # do the contour movement
        time.sleep(1)
        self.battery.chargeBattery(win)

