#!/usr/bin/env python
# coding: utf-8

import time
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps





def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial,enable_nav_map_feed=True, enable_custom_object_detection=True,  show_3d_viewer=True) as robot:
        robot.behavior.say_text("Connected")

        print("connected---------------------------------------------------------------")
        battery_state = robot.get_battery_state()
        print("Robot battery Level: {0}".format(battery_state.battery_level))

        robot.behavior.set_head_angle(degrees(-5.0))
        print("Head Angle Set")
        robot.behavior.set_lift_height(0.0)
        print("Lift Height Set")
        Ausgang = True
        counter = 0
        while Ausgang is False:
            sensor = int(robot.proximity.last_sensor_reading.distance.distance_mm)
            #print(sensor)
            #print(counter)
            if (sensor >= 100 and counter == 0):
                while(sensor>=100):
                    sensor = int(robot.proximity.last_sensor_reading.distance.distance_mm)
                    robot.motors.set_wheel_motors(100,100)
                robot.motors.stop_all_motors()
            if (sensor < 100 ):
                print(counter)
                robot.behavior.turn_in_place(degrees(-90))
                counter = counter + 1
            if (sensor >= 100 and counter != 0):
                robot.behavior.drive_straight(distance_mm(100), speed_mmps(100))
                robot.behavior.turn_in_place(degrees(90))
                print(counter)
                if (sensor < 100):
                    robot.behavior.turn_in_place(degrees(-90))
                    print(counter)
                else:
                    counter = counter - 1;


if __name__ == "__main__":
    main()



