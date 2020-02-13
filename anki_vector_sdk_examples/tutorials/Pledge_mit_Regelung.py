# robot.behavior.say_text("Connected")
#     robot.viewer.show()
#   robot.viewer_3d.show()
robot.behavior.say_text("tt coming home")

print("connected---------------------------------------------------------------")
battery_state = robot.get_battery_state()
print("Robot battery Level: {0}".format(battery_state.battery_level))

robot.behavior.set_head_angle(degrees(-5.0))
print("Head Angle Set")
robot.behavior.set_lift_height(0.0)
print("Lift Height Set")

Ausgang = False
counter = 0

while Ausgang is False:
    robot.behavior.set_head_angle(degrees(-5.0))
    robot.behavior.set_lift_height(0.0)

    sensor_straight = int(robot.proximity.last_sensor_reading.distance.distance_mm)
    print("sensor_straight", sensor_straight)
    print("counter_main", counter)
    print(robot.pose_angle_rad)

    if (sensor_straight >= 200 and counter == 0):
        while (sensor_straight >= 150):
            sensor_straight = int(robot.proximity.last_sensor_reading.distance.distance_mm)
            robot.motors.set_wheel_motors(200, 200)
        else:
            robot.motors.stop_all_motors()
            print("Stop")

    if (sensor_straight < 200):
        robot.behavior.turn_in_place(degrees(-90))
        counter = counter + 1
        print("counter_+1", counter)

    if (sensor_straight >= 200 and counter != 0):
        robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))
        robot.behavior.turn_in_place(degrees(90))
        sensor_wall = int(robot.proximity.last_sensor_reading.distance.distance_mm)
        print("sensor_wall", sensor_wall)
        if (sensor_wall < 200):
            if (sensor_wall < 120):
                robot.behavior.turn_in_place(degrees(-95))
            else:
                robot.behavior.turn_in_place(degrees(-85))
        else:
            counter = counter - 1
            print("counter -1", counter)