# -*- coding: utf-8 -*-
"""
@author: johnoyegbite
"""

# 6.00.2x Problem Set 2: Simulating robots
import math
import random

import ps2_visualize
import pylab
import numpy

##################
# Comment/uncomment the relevant lines, depending on which version of
# Python you have
##################

# For Python 3.5:
# from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5

# For Python 3.6:
from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanedTiles = {}

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        tile_origin = float(math.floor(pos.getX())), float(math.floor(pos.getY()))
        if self.cleanedTiles.get(tile_origin, 0) == 0:
            self.cleanedTiles[tile_origin] = 1  # 0 means dirty 1 means cleaned

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        m, n = float(m), float(n)
        if (m, n) in self.cleanedTiles and not self.cleanedTiles.get((m, n), 0) == 0:
            return True
        return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return math.floor(self.width * self.height)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        total_cleaned_tiles = 0
        for i in range(self.width):
            for j in range(self.height):
                total_cleaned_tiles += self.cleanedTiles.get((float(i), float(j)), 0)
        return total_cleaned_tiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
        return Position(float(x), float(y))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        return (0 <= x < self.width) and (0 <= y < self.height)


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """

    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed

        rand_pos = room.getRandomPosition()
        while not room.isPositionInRoom(rand_pos):
            rand_pos = room.getRandomPosition()
        self.room.cleanTileAtPosition(rand_pos)

        self.direction = 0
        self.position = rand_pos

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return int(self.direction)

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        direction = random.randrange(0, 360)
        update = False
        while not update:
            position = self.getRobotPosition().getNewPosition(direction,
                                                              self.speed)
            if self.room.isPositionInRoom(position):
                self.room.cleanTileAtPosition(position)
                self.setRobotDirection(direction)
                self.setRobotPosition(position)
                update = True
            else:
                direction = random.randrange(0, 360)

        raise NotImplementedError  # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        direction = self.getRobotDirection()
        update = False
        while not update:
            # next line put the robot to a new position
            position = self.getRobotPosition().getNewPosition(direction,
                                                              self.speed)
            if self.room.isPositionInRoom(position):
                self.room.cleanTileAtPosition(position)
                self.setRobotDirection(direction)
                self.setRobotPosition(position)
                update = True
            else:
                direction = random.randrange(0, 360)


# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)
# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        direction = self.getRobotDirection()
        update = False
        while not update:
            # next line put the robot to a new position
            position = self.getRobotPosition().getNewPosition(direction,
                                                              self.speed)
            if self.room.isPositionInRoom(position):
                self.room.cleanTileAtPosition(position)
                direction = random.randrange(0, 360)
                self.setRobotDirection(direction)
                self.setRobotPosition(position)
                update = True
            else:
                direction = random.randrange(0, 360)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    def posTuple(position):
        return (float(math.floor(position.getX())),
                float(math.floor(position.getY())))

    time_steps = []
    num_tiles = width*height  # for total no of tiles
    for trial in range(num_trials):
        # to display the animation and draw a picture of the room
        animation = ps2_visualize.RobotVisualization(num_robots, width,
                                                     height, 0.4)
        # The parameter delay specifies how many seconds the program should
        # pause between frames.
        # The default is 0.2 (that is, 5 frames per second).
        # You can increase this value to make the animation slower or decrease
        # it (0.01 is reasonable),
        # to see many robots cleaning the room at a faster frame rate.
        # delay = 0.2
        # animation = ps2_visualize.RobotVisualization(num_robots, width,
        #                                              height, delay)
        all_robots = []
        room = RectangularRoom(width, height)

        # to create all n(or num_robots) robots with their room and speed
        for robot in range(num_robots):
            all_robots.append(robot_type(room, speed))

        # all robots has not moved at all, and the room is dirty
        num_steps, positions_cleaned = 0, []

        # to make sure that the first time all robots stepped in the room,
        # that position is marked clean
        for robot in all_robots:
            position = robot.getRobotPosition()
            if not posTuple(position) in positions_cleaned:
                positions_cleaned.append(posTuple(position))
        # to keep track of the cleaned part of the room
        while len(positions_cleaned) < min_coverage*num_tiles:
            # to draw a new frame of the animation, for each time-step,
            # before the robot(s) move
            animation.update(room, all_robots)
            for robot in all_robots:
                # move each robot by a step and clean that tile/position
                # either dirty or cleaned
                robot.updatePositionAndClean()
                # get the new position of each robot
                new_pos = robot.getRobotPosition()
                # make sure the  new position of each robot is marked cleaned
                # if and if only if it's not marked earlier
                if not posTuple(new_pos) in positions_cleaned:
                    positions_cleaned.append(posTuple(new_pos))
                num_steps += 1  # count the number of steps of each robot
        animation.done()
        time_steps.append(num_steps)
        positions_cleaned = []
    # I divided by speed to know the step for a unit speed
    mean_time_steps = math.ceil((sum(time_steps) / len(time_steps)) / speed)
    # I divided by num_robots to know the mean_time_steps for a robot
    return float(round(mean_time_steps/num_robots))


# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1, 5, 5, 0.95, 20, StandardRobot))


# print(runSimulation(4, 1.0, 10, 10, 1.0, 1, RandomWalkRobot))

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 5)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 2, 10, 10, 0.5, 20,
                                    StandardRobot))
        times2.append(runSimulation(num_robots, 2, 10, 10, 0.5, 20,
                                    RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width,
              "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200,
                                    StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200,
                                    RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# === Problem 6
# NOTE: If you are running the simulation, you will have to close it
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
# showPlot1("Time it Takes 1-10 Robots To Clean 80% of The Room",
#           "Number of Robots", "Time-Steps")
#
# # Variously shaped means it can be various Rectangle of Square
# showPlot2("Time it Takes 2 Robots To Clean 80% of Variously Shaped Room",
#           "", "Time-Steps")
