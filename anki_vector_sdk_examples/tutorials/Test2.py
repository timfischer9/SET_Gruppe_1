#!/usr/bin/env python

import anki_vector
import time
from anki_vector.util import degrees, distance_mm, speed_mmps
#robot=anki_vector.Robot()
#robot.connect()


def main():
    args = anki_vector.util.parse_command_args()

    # The robot drives straight, stops and then turns around
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("Tina stinkt")
        print("connected---------------------------------------------------------------")
    # Render 3D view of navigation map for 5 seconds
    #robot.viewer.show()
    #robot.vision.enable_custom_object_detection()
        for i in range(10):
            print(i)

            robot.behavior.drive_straight(distance_mm(50), speed_mmps(100))
            print("drive straight 5cm")
            robot.behavior.turn_in_place(degrees(90))
            proximity_data = int(robot.proximity.last_sensor_reading.distance.distance_mm)
            if int(proximity_data) < 50:
                print("Proximity:",int(proximity_data))
                robot.behavior.turn_in_place(degrees(-90))


if __name__ == "__main__":
    main()




