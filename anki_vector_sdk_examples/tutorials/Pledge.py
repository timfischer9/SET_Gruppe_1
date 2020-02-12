#!/usr/bin/env python
# coding: utf-8


import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps
robot = anki_vector.Robot()
robot.connect()
robot.viewer.show()
robot.behavior.set_head_angle(degrees(-5.0))
robot.behavior.set_lift_height(0.0)
Ausgang = False
counter = 0
while Ausgang is False:
    sensor = int(robot.proximity.last_sensor_reading.distance.distance_mm)
    if (sensor >= 50 and counter == 0):    
        robot.behavior.drive_straight(distance_mm(100), speed_mmps(100));
    if (sensor < 50):
        robot.behavior.turn_in_place(degrees(-90))
        counter = counter + 1; 
    if (sensor >= 50 and counter != 0):
        robot.behavior.drive_straight(distance_mm(100), speed_mmps(100))
        robot.behavior.turn_in_place(degrees(90))
        if (sensor < 50):
            robot.behavior.turn_in_place(degrees(-90))
        else:
            counter = counter - 1;



robot.disconnect()





