# robot.behavior.say_text("Connected")
#     robot.viewer.show()
#   robot.viewer_3d.show()
robot.behavior.say_text("i t coming home")

print("connected---------------------------------------------------------------")
battery_state = robot.get_battery_state()
print("Robot battery Level: {0}".format(battery_state.battery_level))

robot.behavior.set_head_angle(degrees(-5.0))
print("Head Angle Set")
robot.behavior.set_lift_height(0.0)
print("Lift Height Set")

Ausgang = False
counter = 0
abort = 0
returnFromWall = False
angle = 0

# Constants
IntervallCheckingDistanceToWall = 6
DegreesCorrectStraightPath = 3
is_ref = 0

print ("Pose of robot", robot.pose)
print ("X, Y coordinates: ", robot.pose.position.x, robot.pose.position.y)


def distance():
    return int(robot.proximity.last_sensor_reading.distance.distance_mm)


def moveForward(dist):
    i = 0
    robot.motors.set_wheel_motors(200, 200)
    while i < dist and distance() >= 150:
        i += 1
        time.sleep(0.1)
    robot.motors.stop_all_motors()


# def moveForward(dist):
#    while distance() >= 180:
#        robot.motors.set_wheel_motors(200, 200)
#    except:
#        robot.motors.stop_all_motors()


def correctStraigthPath():
    if (distance() < 80):
        robot.behavior.turn_in_place(degrees(+90 + DegreesCorrectStraightPath))
    else:
        robot.behavior.turn_in_place(degrees(+90 - DegreesCorrectStraightPath))


def edgeCheck1():
    angel_ref = robot.pose_angle_rad
    print(angel_ref)

    robot.behavior.drive_straight(distance_mm(150), speed_mmps(200))
    time.sleep(1)

    angel_new = robot.pose_angle_rad
    print(angel_new)

    fehler_winkel = (angel_ref - angel_new) * 57.3
    print (fehler_winkel)

    if ((fehler_winkel > 4 or fehler_winkel < -4) and fehler_winkel < 100 and fehler_winkel > -100):
        robot.behavior.drive_straight(distance_mm(-80), speed_mmps(200))
        robot.behavior.turn_in_place(degrees(fehler_winkel))


def edgeCheck():
    print("rechts ", distance())
    robot.behavior.turn_in_place(degrees(-30))
    print("rechts ", distance())
    if (distance() < 100):
        robot.behavior.turn_in_place(degrees(120))
        robot.behavior.drive_straight(distance_mm(60), speed_mmps(200))
        robot.behavior.turn_in_place(degrees(-90))
    else:
        robot.behavior.turn_in_place(degrees(60))
        print("links ", distance())
        if (distance() < 100):
            robot.behavior.turn_in_place(degrees(60))
            robot.behavior.drive_straight(distance_mm(-60), speed_mmps(200))
            robot.behavior.turn_in_place(degrees(-90))
        else:
            robot.behavior.turn_in_place(degrees(-30))

        # def turnAbsolute(a):


#    nonlocal angle
#    angle += a
#    robot.behavior.turn_in_place(degrees(angle), absolute=True)

while Ausgang is False:
    robot.behavior.set_head_angle(degrees(-5.0))
    robot.behavior.set_lift_height(0.0)

    if (is_ref == 0):
        angel_ref = robot.pose_angle_rad
        print(angel_ref)
        is_ref = 1

    # print("sensor_straight", distance())
    # print("counter_main", counter)
    # print("Angle: ", robot.pose_angle_rad)
    # print ("Pose: ", robot.pose)
    # print(angle)

    if (distance() >= 150 and counter == 0):  # go!
        print ("1")
        angel_new = robot.pose_angle_rad
        print(angel_new)
        fehler_winkel = (angel_ref - angel_new) * 57.3
        print (fehler_winkel)
        if (fehler_winkel < 100 and fehler_winkel > -100):
            robot.behavior.turn_in_place(degrees(fehler_winkel))

        while (distance() >= 150):
            robot.motors.set_wheel_motors(200, 200)
        else:
            robot.motors.stop_all_motors()
            print("Stop")

    if (distance() < 150):  # turn and counter +1
        print ("2")
        robot.behavior.turn_in_place(degrees(+90))
        counter = counter + 1
        print("counter_+1", counter)

    if (distance() >= 150 and counter != 0):  # check if i can turn back
        print ("3")
        # robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))
        moveForward(IntervallCheckingDistanceToWall)
        robot.behavior.turn_in_place(degrees(-90))
        # Checking distance to wall
        if (distance() < 150):
            print("sensor_wall", distance())
            correctStraigthPath()
        else:
            edgeCheck()
            counter = counter - 1
            print("counter -1", counter)