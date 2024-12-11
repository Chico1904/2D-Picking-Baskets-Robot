"""
Created on Tue June 7 23:45:00 2022
@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

File with functions responsible for the program interface
"""

from Button import *
from Harve import *
from Obstacles import *
from Basket import *
from random import *


# ---------------------------- Interface Function, common to all implementations ------------------------------
def stationsGenerator(points, win):
    """
    This function generates the docks and docstation by drawing some elements on them and assigning them a color
    :param points: list of points that correspond to station (docks and docstation) points
    :param win: graphics window
    :return: docks, docstation and a lightning bolt that will be drawn on the docstation
    """
    # docks
    docks = [Rectangle(points[0], points[1]), Rectangle(points[2], points[3])]
    docks[0].setFill('brown'), docks[1].setFill('brown')
    docks[0].draw(win), docks[1].draw(win)
    circle_1 = Circle(docks[0].getCenter(), 4)
    circle_1.setFill('orange')
    circle_1.draw(win)
    circle_2 = Circle(docks[1].getCenter(), 4)
    circle_2.setFill('orange')
    circle_2.draw(win)

    # docstation
    docstation = Rectangle(points[4], points[5])
    docstation.setFill('red')
    lightning = Polygon(Point(4, 67), Point(5, 67), Point(3.5, 64.5), Point(4.5, 64.5), Point(2.5, 61), Point(3, 64),
                        Point(2.5, 64))
    lightning.setFill('yellow')

    return docks, docstation, lightning


def interface(implementation_number, win_horizontal, win_vertical, color):
    """
    Function that defines the interface
    :param implementation_number: implementation number
    :param win_horizontal: horizontal dimension of the graphics window
    :param win_vertical: vertical dimension of the graphics window

   This function returns the interface elements, respectively the graphic window (win), the obstacles list (obstacles),
    the exit button (exit_button, applicable in the first 2 implementations), the list with the 2 docks
    (docks), the docstation (where the robot charges the battery), the list with the 6 corners of the docks/docstation,
    and message with the number of baskets that the robot loads (baskets_message) and the font size of the messages (size)
    """

    win = GraphWin(f'{implementation_number}ª Implementação', win_horizontal, win_vertical, autoflush=False)
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color)
    points = [Point(0, 35), Point(10, 45), Point(90, 65), Point(100, 55), Point(0, 60), Point(8, 68)]
    docks, docstation, lightning = stationsGenerator(points, win)

    if implementation_number == 3 or implementation_number == 4:
        # In the last 2 implementations, we will present messages in the interface, one that tells the user that he can
        # exit by clicking 'e' (exit_message) and other with the number of baskets that the robot carries (baskets_message)
        exit_message, baskets_message = Text(Point(50, 95), 'Clique E para sair '), Text(Point(20, 95), f'Baskets=0')
        size = round(
            min(win_horizontal, win_vertical) / 50)  # this relationship creates a font size proportional to win
        exit_message.setSize(size)
        baskets_message.setSize(size)
        docstation.draw(win)
        lightning.draw(win)
        exit_button = None  # In these implementations, we will not have exit button
    else:
        if implementation_number ==2:
            docstation.draw(win)
            lightning.draw(win)
        exit_button = Button(win, 8, 8, Point(8, 92), 'Exit', 'red')
        # In the 2 1st implementations we'll have a fixed size and we won't have the baskets_message
        exit_message, baskets_message, size = None, None, None

    return win, exit_button, docks, docstation, points, exit_message, baskets_message, size


# -------------------------------------------- IMPLEMENTATION 1---------------------------------------------------------

def obstacles_I1_I2(implementation_number):
    """
    This function will create the obstacles needed for the first 2 implementations, returning a list with these
    """
    obstacle_1 = Tree(Point(40, 35), Point(48, 51))
    obstacle_2 = Bush(Point(70, 75), Point(80, 80))
    obstacle_3 = Stone(Point(30, 80), 5)
    obstacle_4 = Grass(Point(70, 15), Point(80, 20))
    obstacle_5 = Stone(Point(30, 15), 5)
    if implementation_number == 1:
        obstacles = [obstacle_1]
    else:
        obstacles = [obstacle_1, obstacle_2, obstacle_3, obstacle_4, obstacle_5]

    return obstacles


# ------------------------------------------IMPLEMENTATION 3------------------------------------------------------

def readObstaclesFile():
    """
    Function that reads the obstacles file, first obtaining a list with the lines of the file (date). remove the lines
    unnecessary and creates another list with several sub-lists. These sub-lists were obtained through the lines
    of the file, which were divided in two, by the white space
    Ex: Bush Rectangle(Point(0,0),Point(5,5)) -> ['Bush' , 'Rectangle(Point(0,0),Point(5,5))']

    :return: the list with the various sub-lists
    """
    infile = open('Ambiente.txt', 'r')
    data = infile.readlines()  # list where each element is a line in the file
    while True:
        # remove all empty lines
        try:
            data.remove('\n')
        except:
            break
    data.pop(0)  # remove the first line from the file
    data.pop(1)  # remove the third line from the file (which became the second)
    main_list = []

    for cont in range(len(data)):
        # For each element of the data list, we separate each line (string) into two, which constitute a new sub-list
        new_data = data[cont].split(" ", 1)
        main_list.append(new_data)  # add the generated sub-list to the main list
    return main_list


def processCircle(obstacle_list):
    """
    Function that, from the data of the file, eliminates unnecessary information and transforms the values
     (which will be used) in real numbers, so that we can define the obstacle, which is
     characterized by a circular zone (Stone)

     :param obstacle_list: an element of the list "list", which has. This element, being a list, has 2 elements:
     the name of the obstacle and the specifications about it
     See ReadFile function for more information about this last list

     :return: the abscissa and ordinate of the center of the circle and its radius
    """

    sub_list_1 = obstacle_list[1].split(
        'Point')  # sub-list that splits the string Circle(Point(x,y),r) into a list with two elements
    sub_list_1.pop(0)  # remove first element from sub-list 1
    sub_list_2 = sub_list_1[0].split(",")  # list with [ (x , y) , radius)], remove the parentheses

    sub_list_3 = sub_list_2[0].split(
        '(')  # split the first element of the list into a list with 2 elements, one empty and the other is the number
    sub_list_3.pop(0)
    x_center = float(sub_list_3[0])  # then we get the x-coordinate of the center of the circle

    sub_list_4 = sub_list_2[1].split(')')
    sub_list_4.pop(1)
    y_center = float(sub_list_4[0])

    sub_list_5 = sub_list_2[2].split(')')
    sub_list_5.pop(1)
    radius = float(sub_list_5[0])

    return x_center, y_center, radius


def processRectangle_or_Oval(obstacle_list):
    """
   Function that, from the data of the file, eliminates unnecessary information and transforms the important values
     (which will be used) in real numbers, so that we can define the obstacle. This will have to be
     characterized by a rectangular area, so it will have to be a rectangle (Grass or Tree) or an ellipse (Bush)

     :param obstacle_list: an element of the list "list", which has. This element, being a list, has 2 elements:
     the name of the obstacle (Ex: Grass, Tree,...) and the specifications about it
     See ReadFile function for more information about this last list

     :return: the abscissa and ordinate of the 2 points that define the rectangular area that characterizes the obstacle
    """
    sub_list_1 = obstacle_list[1].split('Point')
    sub_list_1.pop(0)  # list of the form: ['(x_p1,y_p1),', '(x_p2,y_p2))\n']

    # We will get the values of the 1st point, successively separating the lists in strings and then again in lists
    # In the end, we get a string with the value we want, which we pass to float

    sub_list_2 = sub_list_1[0].split(',')
    sub_list_2.pop(2)  # list of the form ['(x_p1', 'y_p1)']
    sub_list_3 = sub_list_2[0].split('(')
    sub_list_3.pop(0)  # list of the form [x_p1]
    sub_list_4 = sub_list_2[1].split(')')
    sub_list_4.pop(1)  # list of the form [y_p1]
    x_p1 = float(sub_list_3[0])
    y_p1 = float(sub_list_4[0])

    sub_list_5 = sub_list_1[1].split(',')  # list of the form ['(10', '70))\n']
    sub_list_6 = sub_list_5[0].split('(')
    sub_list_6.pop(0)  # list of the form [x_p2]
    sub_list_7 = sub_list_5[1].split(')')  # list of the form ['y_p2))\n']

    y_p2 = float(sub_list_7.pop(0))
    x_p2 = float(sub_list_6[0])

    return x_p1, y_p1, x_p2, y_p2


def choosingConfiguration():
    """
    Function that obtains a list with sub-lists (and the latter correspond to 1 line of the Ambiente file).
     It invokes the functions that "translate" the file and obtain the important information to design the obstacles.
     Then, depending on the name of the obstacle, define it according to the obtained and necessary parameters and add
     each obstacle to a list of obstacles, called obstacles

     :return: list with all obstacles and the dimensions of the graphics window
    """
    main_list = readObstaclesFile()  # list with several lists, each with the specifications of each object (1 line of the doc)
    winConfiguration = main_list.pop(0)  # get a list with 2 elements that define the graphic window
    obstacles = []
    for cont in range(len(main_list)):
        # obstacle_list is a list with 2 elements that define the object (ex: [Bush,Rectangle(Point(0,0), Point(5,5)]
        obstacle_list = main_list[cont]
        obstacle_name = obstacle_list[0]  # string with the name of the obstacle (Ex: Bush)

        if obstacle_name == 'Stone':
            x_center, y_center, radius = processCircle(obstacle_list)
            obstacle = Stone(Point(x_center, y_center), radius)
            obstacles.append(obstacle)
        elif obstacle_name == 'Grass':
            x_p1, y_p1, x_p2, y_p2 = processRectangle_or_Oval(obstacle_list)
            obstacle = Grass(Point(x_p1, y_p1), Point(x_p2, y_p2))
            obstacles.append(obstacle)
        elif obstacle_name == 'Tree':
            x_p1, y_p1, x_p2, y_p2 = processRectangle_or_Oval(obstacle_list)
            obstacle = Tree(Point(x_p1, y_p1), Point(x_p2, y_p2))
            obstacles.append(obstacle)
        elif obstacle_name == 'Bush':
            x_p1, y_p1, x_p2, y_p2 = processRectangle_or_Oval(obstacle_list)
            obstacle = Bush(Point(x_p1, y_p1), Point(x_p2, y_p2))
            obstacles.append(obstacle)
        else:
            continue

    return obstacles, float(winConfiguration[0]), float(winConfiguration[1])


def obstaclesEvaluation(obstacles, robot, docks, docstation):
    """
    1) This function evaluates whether the location of obstacles is correct, that is, if there is no overlap,
    if there is enough space between them for robot movement and if the obstacles are inside the window
    2) In addition, it ensures that obstacles do not coincide with the docks.
    Note: the width and height of the dock are the same as the robot diameter, so we can use these measurements in point 2)

     :param docstation: battery charging dock
     :param docks:list with the two docks
     :param obstacles: list of all obstacles
     :param robot:robot (Harve class instance)
     :return: the evaluation of the location of obstacles in the form of a string, "valid" or "invalid"
    """
    evaluation = 'valid'
    stations = [docks[0], docks[1], docstation]
    for i in range(len(obstacles)):
        # 2 lists, one with the coordinates of the obstacle center and other with the obstacle dimensions
        obs_coord = [obstacles[i].getCenter().getX(), obstacles[i].getCenter().getY()]
        obst_dim = [obstacles[i].getWidth(), obstacles[i].getHeight()]

        if not (0 <= obs_coord[0] - obst_dim[0] / 2 <= 100 and 0 <= obs_coord[0] + obst_dim[0] / 2 <= 100
                and 0 <= obs_coord[1] - obst_dim[1] / 2 <= 100 and 0 <= obs_coord[1] + obst_dim[1] / 2 <= 100):
            evaluation = 'invalid'
            return evaluation

        for j in range(len(stations)):  # see if the obstacles are far from the 3 stations (2 docks, 1 docstation)
            distances = [abs(obstacles[i].getCenter().getX() - stations[j].getCenter().getX()),
                         abs(obstacles[i].getCenter().getY() - stations[j].getCenter().getY())]
            # We get a list with 2 distances (between the obstacle and the stations), one in each component
            # Now we evaluate if the distances between the obstacle and the stations are enough for the robot to pass
            if distances[0] <= obstacles[i].getWidth() / 2 + robot.getWidth() / 2 and \
                    distances[1] <= obstacles[i].getHeight() / 2 + robot.getHeight() / 2:
                evaluation = 'invalid'
                return evaluation

        for j in range(len(obstacles)):  # for each obstacle, see if it is away from all others
            if i != j:  # we can't compare the obstacle with itself, because that would be invalid
                x_dis = abs(obs_coord[0] - obstacles[j].getCenter().getX())
                y_dis = abs(obs_coord[1] - obstacles[j].getCenter().getY())
                x_max = obst_dim[0] / 2 + obstacles[j].getWidth() / 2 + robot.getWidth()
                y_max = obst_dim[1] / 2 + obstacles[j].getHeight() / 2 + robot.getHeight()
                if x_dis <= x_max and y_dis <= y_max:
                    evaluation = 'invalid'
                    return evaluation

    return evaluation


def update_info(win, num_cestos, info):
    # Function that updates the message indicating the basket number that the robot loads as it picks up the baskets
    info.undraw()
    info = Text(Point(20, 95), f'Baskets={num_cestos}')
    info.draw(win)
    return info


# ------------------------------------------IMPLEMENTATION 4------------------------------------------------------

def choosingObstacle(obstacle_prob):
    """
    Function that chooses the type of obstacle, in a random way ( all obstacles have the same probability to be chosen)
    :param obstacle_prob: obstacle probability to be chosen
    :return: the name of the chosen obstacle
    """
    obstacle_chosen = ''
    if obstacle_prob < 0.25:
        obstacle_chosen = 'Tree'
    elif 0.25 <= obstacle_prob < 0.5:
        obstacle_chosen = 'Bush'
    elif 0.5 <= obstacle_prob < 0.75:
        obstacle_chosen = 'Grass'
    elif obstacle_prob >= 0.75:
        obstacle_chosen = 'Stone'

    return obstacle_chosen


def configRectangle(obstacle):
    """
    This function will generate the rectangular obstacle configuration. For this, I need two points (p1 and p2), i.e.,
      the corners of the rectangle that surrounds it
     :param obstacle: obstacle name
     :return: points that define the rectangle that surrounds the obstacle
    """
    while True:  # cycle that only ends when the generated dimensions are valid
        p1 = Point(randrange(1, 100), randrange(1, 100))
        p2 = Point(randrange(1, 100), randrange(1, 100))
        width = abs(p1.getX() - p2.getX())
        height = abs(p1.getY() - p2.getY())

        if width != 0 and height != 0:
            if obstacle == 'Tree':
                # if it's a tree, we want a rectangle with height>width, so it doesn't look disproportionate
                if p1.getX() < p2.getX() and p1.getY() < p2.getY() and 80 > height > width and height / width < 10:
                    break

            elif obstacle == 'Grass' or 'Bush':
                # if it's not a tree,  make sure the dimensions aren't too big and disproportionate
                if p1.getX() < p2.getX() and p1.getY() < p2.getY() and height < 80 and width < 80 \
                        and width / height < 10 and height / width < 10:
                    break

    return p1, p2


def configCircle():
    # This function will generate the circular obstacle configuration. For that, I need the center and radius
    while True:
        # This cycle will end when the dimensions of the defined circle are valid (does not leave the window)
        center = Point(randrange(1, 100), randrange(1, 100))
        radius = randrange(2, 30)  # we limit the radius so that the obstacle is not too big
        if (center.getX() + radius <= 100 and center.getX() - radius >= 0) and \
                (center.getY() + radius <= 100 and center.getY() - radius >= 0):
            break

    return center, radius


def definingObstacle(obstacle_chosen):
    """
    After choosing the type of obstacle and its dimensions, this function creates instances of the classes
    corresponding, that is, it creates the obstacles (objects) themselves.

    :param obstacle_chosen: name of the chosen obstacle
    :return: obstacle as an object, as an instance of a class
    """
    obstacle_chosen = obstacle_chosen.lower()
    if obstacle_chosen == 'tree':
        p1, p2 = configRectangle('Tree')
        obstacle = Tree(p1, p2)

    elif obstacle_chosen == 'bush':
        p1, p2 = configRectangle('Bush')
        obstacle = Bush(p1, p2)

    elif obstacle_chosen == 'grass':
        p1, p2 = configRectangle('Grass')
        obstacle = Grass(p1, p2)

    elif obstacle_chosen == 'stone':
        center, radius = configCircle()
        obstacle = Stone(center, radius)

    return obstacle


def docksOverlap(new_obstacle, docks, docstation):
    """
    This function evaluates whether the obstacle overlaps the dock/doc station. It uses some parameters the
    obstaclesAssessment function. It calculates the minimum distance (x and y) allowed and compares with the distance
    between the obstacle and these objects.

    :param new_obstacle: an obstacle candidate, whose location will have to be assessed
    :param docks: list with the two docks
    :param docstation: battery charging dock
    :return: string that indicates if the new obstacle location is valid or invalid
    """
    assessment = 'valid'
    stations = [docks[0], docks[1], docstation]
    for i in range(len(stations)):
        station_dimensions = [abs(stations[i].getP2().getX() - stations[i].getP1().getX()),
                              abs(stations[i].getP2().getY() - stations[i].getP1().getY())]
        x_distance = abs(new_obstacle.getCenter().getX() - stations[i].getCenter().getX())
        y_distance = abs(new_obstacle.getCenter().getY() - stations[i].getCenter().getY())
        x_min_distance = new_obstacle.getWidth() / 2 + station_dimensions[0] / 2
        y_min_distance = new_obstacle.getHeight() / 2 + station_dimensions[1] / 2

        if x_distance <= x_min_distance and y_distance <= y_min_distance:
            assessment = 'invalid'

    return assessment


def basketsOverlap(baskets_location_list, new_obstacle, robot):
    """
    This function evaluates whether the obstacle overlaps the baskets, whose locations were given by the user,
    through the file. It uses some parameters of the function obstaclesAssessment

    :param baskets_location_list: list with the location of the baskets (if the user introduces the baskets by a file)
    :param new_obstacle: an obstacle candidate, whose location will have to be assessed
    :param robot: robot(Instance of class Harve)
    :return: string that indicates if the new obstacle location is valid or invalid
    """

    assessment = 'valid'

    for i in range(len(baskets_location_list)):
        x_dist_obst_basket = abs(new_obstacle.getCenter().getX() - baskets_location_list[i].getX())
        y_dist_obst_basket = abs(new_obstacle.getCenter().getY() - baskets_location_list[i].getY())
        if x_dist_obst_basket <= new_obstacle.getWidth() / 2 + robot.getWidth() \
                and y_dist_obst_basket <= new_obstacle.getHeight() / 2 + robot.getHeight():
            # the minimum distance is the sum of half of 1 of the obstacle's dimensions and the radius of the robot
            assessment = 'invalid'

    return assessment


def obstaclesOverlap(obstacles, new_obstacle, robot):
    """
   This function evaluates whether the obstacle overlaps the baskets, whose locations were given by the user,
    through the file. It uses some parameters of the function obstaclesAssessment
    This function evaluates whether the obstacle overlaps the other obstacles. It uses some parameters of the
     function obstaclesAssessment.

   :param obstacles: incomplete obstacle list that serves to evaluate the new obstacle
   :param new_obstacle: an obstacle candidate, whose location will have to be assessed
   :param robot: robot(Instance of class Harve)
   :return: string that indicates if the new obstacle location is valid or invalid
   """

    assessment = 'valid'
    for i in range(len(obstacles)):
        x_dis = abs(obstacles[i].getCenter().getX() - new_obstacle.getCenter().getX())
        y_dis = abs(obstacles[i].getCenter().getY() - new_obstacle.getCenter().getY())
        x_min = obstacles[i].getWidth() / 2 + new_obstacle.getWidth() / 2 + robot.getWidth()
        y_min = obstacles[i].getHeight() / 2 + new_obstacle.getHeight() / 2 + robot.getHeight()
        if x_dis <= x_min and y_dis <= y_min:
            # if the distance between obstacles is less than the min. dist., we add the index of the 1st to the list
            assessment = 'invalid'

    return assessment


def obstaclesAssessment(obstacles, new_obstacle, robot, docks, docstation, collection_type, baskets_location_list):
    """
    This function will assess whether the obstacle overlaps the:
    1) docks/docstation (invoke the function docksOverlap)
    3) obstacles (invoke the function obstaclesOverlap)
    2) baskets, if their location is given by a file (invoke the function basketsOverlap)

    :param obstacles: incomplete obstacle list that serves to evaluate the new obstacle
    :param new_obstacle: an obstacle candidate, whose location will have to be assessed
    :param robot: robot(Instance of class Harve)
    :param docks: list with the two docks
    :param docstation: battery charging dock
    :param collection_type: indicates if the user wants to introduce the baskets by a file or by clicks
    :param baskets_location_list: list with the location of the baskets (if the user introduces the baskets by a file)
    """
    assessment = 'valid'

    if collection_type == 'file':
        assessment = basketsOverlap(baskets_location_list, new_obstacle, robot)
        if assessment == 'invalid':
            return assessment

    assessment = docksOverlap(new_obstacle, docks, docstation)
    if assessment == 'invalid':
        return assessment

    assessment = obstaclesOverlap(obstacles, new_obstacle, robot)
    if assessment == 'invalid':
        return assessment

    return assessment


def obstaclesGenerator(robot, docks, docstation, collection_type, baskets_location_list):
    """
    Function that generates the obstacles list. In a while loop, it will successively generate obstacles and add them
    to the list of are valid. When the number of obstacles reaches the target, the cycle stops and the list is returned.

    :param robot: robot(Instance of class Harve)
    :param docks: list with the two docks
    :param docstation: battery charging dock
    :param collection_type: indicates if the user wants to introduce the baskets by a file or by clicks
    :param baskets_location_list: list with the location of the baskets (if the user introduces the baskets by a file)
    :return: a list with valid obstacles
    """

    assessment = 'valid'
    num_obstacles = randrange(3, 7)  # the number of obstacles ranges from 3 to 6
    obstacles = []  # list that, at the end of the cycle, will have all obstacles

    while len(obstacles) < num_obstacles:  # this loop prevents the return of a list with less than 4 obstacles

        obstacle_prob = random()  # the number generated by the random function will define which type of obstacle
        obstacle_chosen = choosingObstacle(obstacle_prob)  # choosing obstacle
        new_obstacle = definingObstacle(obstacle_chosen)  # assignment of features (center, etc) to the obstacle
        assessment = obstaclesAssessment(obstacles, new_obstacle, robot, docks, docstation, collection_type,
                                         baskets_location_list)

        if assessment == 'valid':
            obstacles.append(new_obstacle)

    # At the end of this cycle, I will have the obstacles list, with valid obstacles

    return obstacles
