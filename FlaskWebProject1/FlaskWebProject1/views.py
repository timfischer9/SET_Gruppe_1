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


@app.route('/Pledge_Algo', methods=['POST'])
def Pledge_Algo():
    print ("Pledge Alorithmus wird ausgeführt!")
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
    if(len(Navi)!=0):
        print("Navi-lenghts",len(Navi))
        for i in range(1,len(Navi)):
            print("in schleife")
            print(Navi[len(Navi)-i])
            robot.behavior.go_to_pose(Navi[len(Navi)-i])
    else:
        print("Keine Daten im Navi Array")
    return ""
