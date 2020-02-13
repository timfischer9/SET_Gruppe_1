#!/usr/bin/env python

import anki_vector
import time
from anki_vector.util import degrees, distance_mm, speed_mmps
robot=anki_vector.Robot()
robot.connect()
robot.behavior.say_text("Connected")


def main():

       # Use a "for loop" to repeat the indented code 4 times
       # Note: the _ variable name can be used when you don't need the value

    for _ in range(4):
       print("Drive Vector straight...")
       robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))

       print("Turn Vector in place...90")
       robot.behavior.turn_in_place(degrees(90))
       print("Turn Vector in place...-180")
       robot.behavior.turn_in_place(degrees(-180))
       print("Turn Vector in place...90")
       robot.behavior.turn_in_place(degrees(90))
    robot.disconnect()



if __name__ == "__main__":
    main()





