# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:45:00 2022
@author: Francisco Miranda, nº 102494
         Tiago Videira, nº 102560
         Grupo 11

Main program file
"""

from Interface import *


# -------------------------------------------- IMPLEMENTATION 1---------------------------------------------------------


def closerDock(latest_point, points, docks):
    """
   Function that evaluates the nearest dock, after the robot picks up the basket.
    :param latest_point: center of the final basket (final input_point)
    :param points: list of points with the corners of the docks
    :param docks: list with the two docks
    """
    # We calculate the distance between the last pick-up point and the docks, setting the end point as the closest point
    d1 = sqrt((latest_point.getX() - (points[0].getX() + points[1].getX()) / 2) ** 2 + (
            latest_point.getY() - (points[0].getY() + points[1].getY()) / 2) ** 2)
    d2 = sqrt((latest_point.getX() - (points[2].getX() + points[3].getX()) / 2) ** 2 + (
            latest_point.getY() - (points[2].getY() + points[3].getY()) / 2) ** 2)

    if d1 <= d2:
        final_point = docks[0].getCenter()
    else:
        final_point = docks[1].getCenter()

    return final_point


def evaluationInput_point(input_points, obstacles, robot):
    """
   Function that evaluates if the input_point (i.p) is valid, that is, if:

    1) is not very close to the edge of the graphics window, which would cause the robot to exit it (1st 'for' cycle)

    2) is far enough away from obstacles to pick up the basket (2nd 'for' cycle). For this, we calculate the
    distance between the i.p and the center of the obstacle, in x (distance_x) and in y (distance_y) and see if they are
    less than minimum distance (which is the sum of half the width/height of the robot and half the width/height of the
     obstacle)

    :param input_points: list of input points (i.p) given by the user
    :param obstacles: obstacle list
    :param robot: instance of the Harve class (our robot). We need its attributes (height and width)
           to set the minimum distance between each obstacle
    :return: a string that will tell you if the point is valid (evaluation_input_point = "") or invalid
             (evaluation_input_point = "invalid point")
    """
    evaluation_input_point = "valid point"
    for i in range(len(input_points)):  # loop that loops through all input points list
        if not (robot.getWidth() / 2 <= input_points[i].getX() <= 100 - robot.getWidth() / 2 and
                robot.getHeight() / 2 <= input_points[i].getY() <= 100 - robot.getHeight() / 2):
            # If the distance between the i.p and the window is < half of 1 of the robot's dimensions, it would have to
            # leave the graphic window. Therefore, the i.p is invalid and we break the cycle
            evaluation_input_point = "invalid point"
            break

        for j in range(len(obstacles)):
            # For each i.p we will assess whether they are far enough away from obstacles
            distance_x = abs(input_points[i].getX() - obstacles[j].getCenter().getX())
            distance_y = abs(input_points[i].getY() - obstacles[j].getCenter().getY())
            if (distance_x <= obstacles[j].getWidth() / 2 + robot.getWidth() / 2 + 0.02) \
                    and (distance_y <= obstacles[j].getHeight() / 2 + robot.getHeight() / 2 + 0.02):
                evaluation_input_point = "invalid point"
                break
            # if the distance is large enough, evaluation_input_point becomes an empty string

        if evaluation_input_point == "invalid point":
            break

    return evaluation_input_point


def input_pointsUpdate(input_points, obstacles, robot, win, cont, baskets):
    """
    This function will update the list of input_points depending on whether they are valid or not.

     :param input_points: list of input points (i.p's) given by the user
     :param obstacles: list of obstacles
     :param robot: robot (Harve class instance)
     :param win: graphical window
     :param cont: count variable, which will only increase if i.p is valid
     :param baskets: list of baskets whose locations have been defined by the user
     :return: list of input_points and baskets (updated) and count variable
    """
    evaluation_input_point = evaluationInput_point(input_points, obstacles, robot)
    if evaluation_input_point == "invalid point":
        # if the i.p is invalid, we remove it from the list and the user will choose another point
        input_points.pop(-1)
        input_points.append(win.getMouse())

    else:
        # if the i.p is valid, we define a basket and draw it with the center in the i.p, adding it to the list of baskets
        basket = Basket(2, 'orange', input_points[cont])
        baskets.append(basket)
        basket.draw(win)
        # The user can choose another point and, as the previous one was valid, the count variable increments
        input_points.append(win.getMouse())
        cont += 1

    return input_points, baskets, cont


def movement_I1_I2(input_points, robot, baskets, win, points, docks, docstation, obstacles, battery):
    """
    This function is responsible for the robot's movement. Going through the list of input points (except the last one, as
     it only serves to trigger the robot's movement, not counting as a collection point), the robot will move
     until the i.p, collect the basket and, at the end, return to the nearest dock.

     :param input_points: list of input points (i.p) given by the user
     :param robot: robot (Harve class instance)
     :param baskets: list of baskets whose locations have been defined by the user
     :param win: graphical window
     :param points: list of points with the corners of the docks and docstation
     :param docks: list with the two docks
     :param docstation: battery charging dock
     :param obstacles: list of obstacles
     :param battery: string that indicates if we want to the battery to be activated or not
    """
    cont = 0
    for cont in range(len(input_points) - 1):  # loop through the list of input_points (except the last one)
        # Each cycle corresponds to the collection of 1 basket

        robot.movementMain(input_points[cont], obstacles, win, docstation.getCenter(), battery)
        baskets[cont].undraw()  # Arriving at the destination, the basket in the window will be deleted
        time.sleep(0.5)  # The robot waits 0.5s
        robot.drawBasket(
            win)  # The basket attached to the robot is drawn, in order to simulate the collection of the basket

    # Once all the baskets have been collected, the robot will take them to the nearest dock
    final_point = closerDock(input_points[cont], points, docks)
    robot.movementMain(final_point, obstacles, win, docstation.getCenter(), battery)
    robot.undrawBasket()


def processingInput_I1_I2(obstacles, robot, exit_button, win, points, docks, docstation, battery):
    """
    This function processes what happens from the appearance of the interface to the start of the robot's movement.
    The main "while" loop will only end when the exit button is clicked.
    At each iteration, the function evaluates the first i.p given by the user. Then, if valid, the function will process
    all other i.p until the user clicks on the robot. Finally, the robot collects the baskets

     :param obstacles:list with obstacles
     :param robot: robot (Harve class instance)
     :param exit_button:
     :param win:graphic window
     :param points:point list with dock corners
     :param docks:list with the two docks
     :param docstation:battery charging dock
     :param battery: string that indicates if we want to the battery to be activated or not
    """

    while True:  # while there is no break, we create the list of input_points, taking into account the exit point
        # Each iteration corresponds to a complete collection of baskets
        exit = False  # variable that defines whether the exit button was clicked (False) or not (True)
        input_points = [win.getMouse()]
        evaluation = evaluationInput_point(input_points, obstacles, robot)

        if evaluation == "ponto inválido":
            pass

        else:  # if the first point is not invalid, we start the movement
            baskets, cont = [], 0
            while not ((robot.getCenter().getX() - robot.getWidth() <= input_points[cont].getX() <= robot.getCenter().getX() + robot.getWidth())
                   and (robot.getCenter().getY() - robot.getHeight() <= input_points[cont].getY() <= robot.getCenter().getY() + robot.getHeight())):
                # as long as the point clicked by the user is not in the robot, we will add the points to a list
                if exit_button.clicked(input_points[cont]):
                    exit = True
                    win.close()
                    break
                input_points, baskets, cont = input_pointsUpdate(input_points, obstacles, robot, win, cont, baskets)

            if exit:
                break  # if the exit button is clicked, we stop the main loop

            # we obtain a list of points, where the last one doesn't count as it is the movement's initialization point
            movement_I1_I2(input_points, robot, baskets, win, points, docks, docstation, obstacles, battery)


def implementation_1(velocity, background_color):
    """
    This function will execute the first implementation. Through a while loop, we will execute the robot's movement,
    in which each cycle corresponds to the input_point (i.p) processing and consequent movement of the robot,
    first to the i.p and then to the dock
    """
    obstacles = obstacles_I1_I2(1)
    # get the interface with all elements
    win, exit_button, docks, docstation, points, exit_message, baskets_message, size = interface(1, 600, 600, background_color)
    dock_1_center = Point((points[0].getX() + points[1].getX()) / 2, (points[0].getY() + points[1].getY()) / 2)

    robot = Harve(win, 4, dock_1_center, 'black', velocity)
    robot.undrawBattery()

    for cont in range(len(obstacles)):
        obstacles[cont].draw(win)

    processingInput_I1_I2(obstacles, robot, exit_button, win, points, docks, docstation, 'battery deactivated')
    # this function will process what happens from the appearance of the interface to the start of the robot's movement


# -------------------------------------------- IMPLEMENTATION 2-----------------------------------------------------


def implementation_2(velocity, background_color):
    """
    Main function of implementation 2, which defines the graphic window with all its elements (obstacles, robot,...)
    and invokes the processingInput_I2, responsible for the implementation itself
    """
    obstacles = obstacles_I1_I2(2)
    # get the interface with all elements
    win, exit_button, docks, docstation, points, exit_message, baskets_message, size = interface(2, 600, 600, background_color)
    dock_1_center = Point((points[0].getX() + points[1].getX()) / 2, (points[0].getY() + points[1].getY()) / 2)

    robot = Harve(win, 4, dock_1_center, 'black', velocity)

    for cont in range(len(obstacles)):
        obstacles[cont].draw(win)

    processingInput_I1_I2(obstacles, robot, exit_button, win, points, docks, docstation, 'battery activated')
    # this function will process what happens from the appearance of the interface to the start of the robot's movement


# ------------------------------------------IMPLEMENTATION  3------------------------------------------------------

def handle_key_mouse(win, obstacles, robot):
    """
   Function responsible for analyzing, at the beginning of each complete robot movement, whether the user presses the button
     exit of the program (E) or if you click on a valid place to place the basket, returning the clicked point and the key.
    """
    global initial_input_point
    global key

    while True:  # this cycle only ends when a valid point is clicked or when the E key is pressed

        pt = win.checkMouse()
        if pt:
            evaluation = evaluationInput_point([pt], obstacles, robot)
            if evaluation != "invalid point":
                initial_input_point = pt
                break

        key = win.checkKey()
        if key == 'e':
            initial_input_point = Point(0, 0)
            break

    return key, initial_input_point


def pop_up_message(text, width, height):
    """
    Function that makes a message appear in a different graphic window, closing after 1.5 seconds
    :param text: message that appears in the window
    :param width: width of the window
    :param height: height of the window
    :return:
    """
    win = GraphWin("Clique para sair", width, height)
    win.setCoords(0, 0, 100, 100)
    message = Text(Point(50, 50), text)
    message.draw(win)
    time.sleep(1.5)
    win.close()


def movement_I3_I4(input_points, robot, baskets_number, baskets, obstacles, win, points, docks, docstation,
                   message_2, size):
    """
    Function that performs the movement of the robot to the collection point, as well as the collection of the baskets
     and the movement to the dock

     :param size:size of the letters that appear in the interface
     :param docstation:battery charging dock
     :param docks:list with the two docks
     :param points:point list with dock and docstation corners
     :param input_points:list of points given by the user
     :param robot:robot(Instance of class Harve)
     :param baskets_number:baskets that the robot currently has
     :param baskets:list of user-defined baskets
     :param obstacles:list of obstacles (given by file)
     :param win:graphic window
     :param message_2:message containing the number of baskets and which is updated with each collection
    """
    docstation_center = docstation.getCenter()
    cont = 0
    for cont in range(len(input_points) - 1):  # loop through the list of input_points, except the last one
        robot.movementMain(input_points[cont], obstacles, win, docstation_center, 'battery activated')
        # execution of the movement to the point defined by the user
        baskets_number += 1
        # Update of the message that indicates the number of baskets (one more basket was collected)
        message_2 = update_info(win, baskets_number, message_2)
        message_2.setSize(size)
        baskets[cont].undraw()
        time.sleep(0.5)
        robot.drawBasket(win)

    final_point = closerDock(input_points[cont], points, docks)  # dock choice + next
    robot.movementMain(final_point, obstacles, win, docstation_center, 'battery activated')
    robot.undrawBasket()  # At the end of the movement, the basket that is attached to the robot is deleted
    baskets_number = 0
    # Update the number of baskets to 0
    message_2 = update_info(win, baskets_number, message_2)
    message_2.setSize(size)

    return message_2


def processingInput_I3_I4(robot, win, obstacles, message_2, points, docks, docstation, size, collection_type,
                          baskets_list):
    """
    This function processes what happens from the appearance of the interface to the start of the robot's movement.
    The main "while" loop will only end when the 'E' key is pressed.
    At each iteration, the function evaluates the first i.p given by the user. Then, if valid, the function
    will process all other i.p until the user clicks on the robot. Finally, the robot collects the baskets

    :param robot: robot(Instance of class Harve)
    :param win: graphical window
    :param obstacles: obstacle list
    :param message_2: message indicating the number of baskets the robot is currently carrying
    :param points: list of dock and docstation corners
     param docks: list with the two docks
    :param docstation: robot battery charging zone
    :param size: size of the letters that appear in the interface
    :param collection_type: indicates if the user wants to introduce the baskets by a file or by clicks (4th implementation)
    :param baskets_list: list with the location of the baskets (if the user introduces the baskets by a file)
    :return: list of input points (checked)
    """
    while True:  # each repetition corresponds to a complete robot movement

        key, initial_inputpoint = handle_key_mouse(win, obstacles, robot)
        if key == 'e':
            win.close()
            input_points, cont, baskets = [], 0, []  # this assignement is needed so that it does not give error
            break

        input_points = [initial_inputpoint]
        cont = 0
        baskets = []
        num_cestos = 0  # variable that counts the number of baskets that the robot currently has
        if collection_type == 'file':
            for i in range(len(baskets_list)):
                cesto = Basket(2, 'orange', baskets_list[i])
                baskets.append(cesto)
                cesto.draw(win)

        while not ((robot.getCenter().getX() - robot.getWidth() <= input_points[cont].getX() <= robot.getCenter().getX() + robot.getWidth())
                and (robot.getCenter().getY() - robot.getHeight() <= input_points[cont].getY() <= robot.getCenter().getY() + robot.getHeight())):
            # as long as the point clicked by the user is not in the robot, let's add the valid points to the list
            if collection_type != 'file':  #
                input_points, baskets, cont = input_pointsUpdate(input_points, obstacles, robot, win, cont, baskets)
            else:
                p = win.getMouse()
                input_points.append(p)
                cont += 1

        if collection_type == 'file':
            input_points = baskets_list
            input_points.append("")
        # We execute the function that moves the robot and return message_2, so that it is updated in the next iteration
        message_2 = movement_I3_I4(input_points, robot, num_cestos, baskets, obstacles, win, points, docks, docstation,
                                   message_2, size)

    return input_points, cont, baskets


def implementation_3(velocity, background_color):
    """
    Function that calls all functions necessary for the execution of implementation 3
     Start by drawing the obstacles and the robot in the graphic window, evaluating the first
     If they are all in valid locations, start the implementation itself ( i3_secondary ),
     which will execute the processing of input points and the consequent movement of the robot
    """
    try:
        obstacles, win_horizontal, win_vertical = choosingConfiguration()
        # the next structure is to avoid the program error in case the window size is invalid
        size = round(min(win_horizontal, win_vertical) / 50)
        if not (10 <= size <= 30):
            # if the window dimensions are too disproportionate, this is reflected in the font size
            pop_up_message('Dimensões da Janela Inválidas, insira outras', 400, 200)

        else:
            win, exit_button, docks, docstation, points, exit_message, baskets_message, size \
                = interface(3, win_horizontal, win_vertical, background_color)
            p7 = Point((points[0].getX() + points[1].getX()) / 2, (points[0].getY() + points[1].getY()) / 2)
            robot = Harve(win, 4, p7, 'black', velocity)
            # in this implementation we have to ensure that the obstacles are properly located
            evaluation = obstaclesEvaluation(obstacles, robot, docks, docstation)

            if evaluation == 'invalid':  # if the obstacle location is wrong, the program will not run
                pop_up_message('Localização dos obstáculos inválida, insira outra', 400, 200)
                win.close()

            else:  # if the location of the obstacle is correct, we draw them and run the processingInput_I3_I4 function
                for cont in range(len(obstacles)):
                    obstacles[cont].draw(win)
                exit_message.draw(win)
                baskets_message.draw(win)
                processingInput_I3_I4(robot, win, obstacles, baskets_message, points, docks, docstation, size, 'mouse clicks', [])
                win.close()
    except:
        pop_up_message('Não foi possível a leitura do ficheiro, consulte o manual de utilzador', 500, 300)


# -----------------------------------------IMPLEMENTATION  4-----------------------------------------------------------
def readBasketsFile(robot):
    """
    Function that reads the file 'Limpeza.txt and returns a list with the centers of the valid baskets
    :param: robot, an instance of the class Harve. It will allow evaluating the location of the baskets
    :return:baskets_list: a list with the points representing the centers of the baskets
    """
    infile = open('Limpeza.txt', 'r')
    data = infile.readlines()
    data.pop(0)  # the first line of the text file is not useful
    while True:  # this cycle will remove the empty lines
        try: data.remove('\n')
        except: break

    main_list = []
    for i in range(len(data)):
        main_list.append(data[i].split())  # list with sub-lists that consist of a line of the file
    baskets_list = []
    for i in range(len(main_list)):
        basket_n = main_list[i]  # Ex: basket_n = ['20', '10']
        x = float(basket_n[0])
        y = float(basket_n[1])
        baskets_list.append(Point(x, y))  # we add a point of coordinates x and y to the list of baskets

    i = 0
    while True:
        # this cycle will remove the invalid baskets (with negative coordinates, for example)
        try:
            if not (robot.getWidth() / 2 <= baskets_list[i].getX() <= 100 - robot.getWidth() / 2) \
                    or not (robot.getHeight() / 2 <= baskets_list[i].getY() <= 100 - robot.getHeight() / 2):
                baskets_list.pop(i)
            else:
                i += 1
        except: break

    return baskets_list


def collectionTypeDecision():
    """
    Creates a graphical window for the user to choose whether to place the baskets by mouse clicks or by file
    :return: collection_type, a string variable that indicates the user choice
    """
    win = GraphWin('Como pretende escolher a localização dos cestos?', 400, 400)
    win.setCoords(0, 0, 100, 100)
    button_1 = Button(win, 20, 30, Point(30, 50), 'Ficheiro', 'yellow')
    button_2 = Button(win, 20, 30, Point(70, 50), 'Cliques de rato', 'yellow')
    while True:
        p = win.getMouse()
        if button_1.clicked(p):
            collection_type = 'file'
            win.close()
            break
        elif button_2.clicked(p):
            collection_type = 'mouse clicks'
            win.close()
            break
    return collection_type


def implementation_4(velocity, background_color):
    """
     Main function of implementation 4, which defines the interface and calls the i3_secondary function, which, as in
     implementation 3, will run the implementation itself.
     """
    collection_type = collectionTypeDecision()
    win, exit_button, docks, docstation, points, exit_message, baskets_message, size = interface(4, 600, 600, background_color)
    p7 = Point((points[0].getX() + points[1].getX()) / 2, (points[0].getY() + points[1].getY()) / 2)
    robot = Harve(win, 4, p7, 'black', velocity)

    try:
        if collection_type == 'file':
            baskets_list = readBasketsFile(robot)
        else:
            baskets_list = []
        obstacles = obstaclesGenerator(robot, docks, docstation, collection_type, baskets_list)
        for cont in range(len(obstacles)):
            obstacles[cont].draw(win)
        exit_message.draw(win)
        baskets_message.draw(win)
        # The next structure is used to close the program when the user tries to do something after the robot has collected
        # every basket (in case of having inserted them by file)
        try:
            processingInput_I3_I4(robot, win, obstacles, baskets_message, points, docks, docstation, 12, collection_type, baskets_list)
        except:
            win.close()
    except:
        pop_up_message('Não foi possível a leitura do ficheiro, consulte o manual de utilzador', 500, 300)

    win.close()


# ---------------------------------------------------------------------------------------------------------------------

def velocityConverter(velocity_percentage):
    """
    Function that receives the value given by the user (from 1 to 100) and converts it into the value of the
    robot's real velocity. The mathematical expression used takes into account the maximum and minimum allowed values
    of the velocity ( velocity_percentage = 1 -> velocity = 2 ; velocity_percentage = 100 -> velocity = 20)

    :param velocity_percentage: value given by the user (represents the robot velocity, in percentage)
    :return: robot's real velocity
    """
    if 1 <= velocity_percentage <= 100:
        velocity = (18 / 99) * velocity_percentage + 20 / 11
    elif velocity_percentage < 1:
        velocity = 2
    else:
        velocity = 20
    return velocity


def getConfigurations(win, input_box, buttons, colors):
    """
    Function that creates 6 buttons so that the user can choose the color, apply the settings and exit the settings window
    Regarding the color, it receives and returns the string corresponding to the color.

    As for the speed, it will receive 'input_value' -> this is the string that the user entered. If it's a number,
    then we convert it to a number(float). If it's not, then we set 'velocity_percentage' = 45. 'velocity_percentage'
    is a value (preferably between 1 and 100) that's transformed in the real velocity value, through another function

    :param win: graphical window of the settings
    :param input_box: input box for the user to enter the desired speed
    :param buttons: list with the six buttons (instances of the class Button)
    :param colors: list with 6 strings that represent the button colors
    :return: The background color and the robot velocity, configurations chosen by the user
    """
    background_color, velocity = 'green1', 10  # these are the default settings
    while True:
        p = win.checkMouse()
        if p is not None:  # if the user has clicked somewhere in the graphics window, we verify

            for cont in range(4):
                # check if the user clicked on any background color button and, if so, the background color is set
                if buttons[cont].clicked(p):
                    background_color = colors[cont]

            if buttons[4].clicked(p):
                # if the user clicks the fifth button then he wants to apply the configurations
                input_value = input_box.getText()
                if input_value.isnumeric():
                    velocity_percentage = float(input_value)  # if input is a number, we convert it to a float
                else:
                    velocity_percentage = 45  # value that makes robot's real velocity = 10

                velocity = velocityConverter(velocity_percentage)
                pop_up_message('Configurações alteradas', 300, 300)

            elif buttons[5].clicked(p):
                # if the user clicks the sixth button then he wants to exit the configurations window
                break

    return background_color, velocity


def configurations():
    """
    Function that defines the graphical window of the settings, implementing the buttons and text messages.
    It also invokes the function that will  receive the user's settings
    :return: The background color and the robot velocity, configurations chosen by the user
    """
    # graphics window definition
    win = GraphWin('Configurations', 800, 600)
    win.setCoords(0, 0, 100, 100)
    text = Text(Point(50, 95), "Escolha as configurações do programa")
    text.setSize(20)
    text.draw(win)

    # velocity input definition
    input_box = Entry(Point(40, 80), 5)
    input_box.draw(win)
    vel_message_1 = Text(Point(30, 80), "Velocidade =")
    vel_message_1.draw(win)
    vel_message_2 = Text(Point(60, 80), "(intoduza um valor entre 1 e 100)")
    vel_message_2.draw(win)

    # background color input definition
    color_message = Text(Point(50, 55), 'Escolha a cor para o fundo da interface')
    color_message.setSize(15)
    color_message.draw(win)
    points = [Point(20, 40), Point(40, 40), Point(60, 40), Point(80, 40), Point(30, 10),
              Point(70, 10)]  # list of button centers
    buttons = []
    message = ['AMARELO', 'LARANJA', 'AZUL', 'ROXO', 'APLICAR', 'SAIR']  # list of button labels
    colors = ['yellow', 'orange', 'blue', 'purple', 'red', 'red']  # list of button colors

    for cont in range(6):
        # we create 6 button objects and add them to the buttons list
        button = Button(win, 10, 15, points[cont], message[cont], colors[cont])
        buttons.append(button)

    background_color, velocity = getConfigurations(win, input_box, buttons, colors)

    win.close()

    return background_color, velocity


def menu():
    # This function is the main menu, where the user chooses which implementation he wants

    win = GraphWin('Menu', 800, 600)
    win.setCoords(0, 0, 100, 100)
    menu_message = Text(Point(50, 85), 'MENU')
    menu_message.setSize(30)
    menu_message.draw(win)
    p1, p2, p3, p4, p5, p6 = Point(25, 60), Point(75, 60), Point(25, 40), Point(75, 40), Point(25, 20), Point(75, 20)
    button_I1 = Button(win, 10, 20, p1, '1ªImplementação', 'green')
    button_I2 = Button(win, 10, 20, p2, '2ªImplementação', 'green')
    button_I3 = Button(win, 10, 20, p3, '3ªImplementação ', 'green')
    button_I4 = Button(win, 10, 20, p4, '4ªImplementação  ', 'green')
    config_button = Button(win, 10, 20, p5, 'Configurações', 'white')
    exit_button = Button(win, 10, 20, p6, 'Exit', 'red')
    return button_I1, button_I2, button_I3, button_I4, config_button, exit_button, win


def main():
    """
    Main function that will call the function associated with the implementation chosen by the user in the menu
    """
    button_I1, button_I2, button_I3, button_I4, config_button, exit_button, win = menu()
    velocity = 10
    background_color = 'green1'
    while True:
        p = win.getMouse()
        if button_I1.clicked(p):
            implementation_1(velocity, background_color)
        elif button_I2.clicked(p):
            implementation_2(velocity, background_color)
        elif button_I3.clicked(p):
            implementation_3(velocity, background_color)
        elif button_I4.clicked(p):
            implementation_4(velocity, background_color)
        elif config_button.clicked(p):
            background_color, velocity = configurations()
        elif exit_button.clicked(p):
            win.close()
            break


main()
