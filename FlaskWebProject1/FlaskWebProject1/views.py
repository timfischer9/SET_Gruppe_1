"""
Routes and views for the flask application.
"""
import time
import numpy
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app

robot=anki_vector.Robot(enable_nav_map_feed =True)

Navi=[]
drehungen=0
abort = 0
returnFromWall = False
angle = 0
angle_ref=0
Ausgang=False
    # Constants
IntervallCheckingDistanceToWall = 6
DegreesCorrectStraightPath = 3
is_ref = 0


@app.route('/')

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/connect_fkt', methods=['POST'])
def connect_fkt():
    robot.connect()

    print ("Connected!")
    robot.behavior.say_text("Connected")
    return ""

@app.route('/Disconnect_fkt', methods=['POST'])
def Disconnect_fkt():
    robot.behavior.say_text("Bye Bye")
    robot.disconnect()
    print ("Disconnected!")
    return ""


@app.route('/test1', methods=['POST'])
def test1():
    print ("Moving!")
    robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))

    return ""

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


def correctStraigthPathl():
    global IntervallCheckingDistanceToWall
    global DegreesCorrectStraightPath
    global is_ref
    if (distance() < 80):
        robot.behavior.turn_in_place(degrees(+90 + DegreesCorrectStraightPath))
    else:
        robot.behavior.turn_in_place(degrees(+90 - DegreesCorrectStraightPath))

def correctStraigthPathr():
    if (distance() < 80):
        robot.behavior.turn_in_place(degrees(-90 - DegreesCorrectStraightPath))
    else:
        robot.behavior.turn_in_place(degrees(-90 + DegreesCorrectStraightPath))

def edgeCheck1():
    global angel_ref
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

@app.route('/pledgelfkt', methods=['POST'])
def pledgelfkt():
    robot.behavior.say_text("i t coming home")
    global IntervallCheckingDistanceToWall
    global DegreesCorrectStraightPath
    global is_ref
    global Ausgang
    IntervallCheckingDistanceToWall = 6
    DegreesCorrectStraightPath = 3
    is_ref = 0
    print("connected---------------------------------------------------------------")
    battery_state = robot.get_battery_state()
    print("Robot battery Level: {0}".format(battery_state.battery_level))

    robot.behavior.set_head_angle(degrees(-5.0))
    print("Head Angle Set")
    robot.behavior.set_lift_height(0.0)
    print("Lift Height Set")

    Ausgang = False
    counter = 0


    print ("Pose of robot", robot.pose)
    print ("X, Y coordinates: ", robot.pose.position.x, robot.pose.position.y)
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
            setPoint()
            print("counter_+1", counter)

        if (distance() >= 150 and counter != 0):  # check if i can turn back
            print ("3")
            # robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))
            moveForward(IntervallCheckingDistanceToWall)
            robot.behavior.turn_in_place(degrees(-90))
            # Checking distance to wall
            if (distance() < 150):
                print("sensor_wall", distance())
                correctStraigthPathl()
            else:
                edgeCheck()
                counter = counter - 1
                setPoint()
                print("counter -1", counter)
    return ""



@app.route('/pledgerfkt', methods=['POST'])
def pledgelrkt():
    robot.behavior.say_text("i t coming home")
    global IntervallCheckingDistanceToWall
    global DegreesCorrectStraightPath
    global is_ref
    global Ausgang
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
            robot.behavior.turn_in_place(degrees(-90))
            counter = counter + 1
            setPoint()
            print("counter_+1", counter)

        if (distance() >= 150 and counter != 0):  # check if i can turn back
            print ("3")
            # robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))
            moveForward(IntervallCheckingDistanceToWall)
            robot.behavior.turn_in_place(degrees(90))
            # Checking distance to wall
            if (distance() < 150):
                print("sensor_wall", distance())
                correctStraigthPathr()
            else:
                edgeCheck()
                counter = counter - 1
                setPoint()
                print("counter -1", counter)


    return ""

@app.route('/stopw', methods=['POST'])
def stopw():
    print ("Stop")
    robot.motors.stop_all_motors()
    return ""

@app.route('/startw', methods=['POST'])
def startw():
    print ("Start")
    robot.motors.set_wheel_motors(200,200)
    return ""

@app.route('/startd', methods=['POST'])
def startd():
    print ("turn right")
    robot.motors.set_wheel_motors(100,-100)
    return ""

@app.route('/starta', methods=['POST'])
def starta():
    print ("turn right")
    robot.motors.set_wheel_motors(-100,100)
    return ""

@app.route('/starts', methods=['POST'])
def starts():
    print ("bwd")
    robot.motors.set_wheel_motors(-200,-200)
    return ""

@app.route('/home_fkt', methods=['POST'])
def home_fkt():
    print ("Coming Home!")
    robot.behavior.set_eye_color(0.57, 1.00)

    return ""


@app.route('/MapFkt', methods=['POST'])
def MapFkt():
    print ("Map activated!")
    robot.viewer_3d.show()
    return ""

@app.route('/CamFkt', methods=['POST'])
def CamFkt():
    print ("Cam activated!")
    robot.viewer.show()
    return ""

@app.route('/setPoint', methods=['POST'])
def setPoint():
    Navi.append(robot.pose)
    #drehungen=drehungen+1
    print("Punkt gesetzt")
    print(Navi[len(Navi)-1])
    return ""

@app.route('/bwdstep', methods=['POST'])
def bwdstep():
    print("going back")
    global Ausgang
    Ausgang=True
    if(len(Navi)!=0):
        print("Navi-lenghts",len(Navi))
        for i in range(1,len(Navi)):
            print("in schleife")
            print(Navi[len(Navi)-i])
            robot.behavior.go_to_pose(Navi[len(Navi)-i])
    else:
        print("Keine Daten im Navi Array")
    return ""
