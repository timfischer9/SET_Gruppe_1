#!/usr/bin/env python
# coding: utf-8

import time
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps





def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial, enable_custom_object_detection=True, enable_nav_map_feed=True) as robot:
        robot.behavior.say_text("Connected")
        robot.viewer_3d.show()
        robot.viewer.show()
        robot.world.connect_cube()
        print ("Connected to Cube")
        robot.behavior.say_text("Connected to Cube")
        robot.behavior.set_eye_color(0.57, 1.00)

        if robot.world.connected_light_cube:
            robot.behavior.say_text("Going to Cube")
            robot.behavior.dock_with_cube(robot.world.connected_light_cube)
        else:
            robot.behavior.say_text("Error")
        if robot.world.connected_light_cube:
            robot.behavior.say_text("Going to Cube")
            robot.behavior.go_to_object(robot.world.connected_light_cube, distance_mm(70.0))


if __name__ == "__main__":
    main()



