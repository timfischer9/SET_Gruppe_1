"""
Routes and views for the flask application.
"""
import time

import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app

robot=anki_vector.Robot()

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
        sensor = int(robot.proximity.last_sensor_reading.distance.distance_mm)
        if (sensor >= 200 and counter == 0):
            while(sensor>=150):
                sensor = int(robot.proximity.last_sensor_reading.distance.distance_mm)
                robot.motors.set_wheel_motors(200,200)
            robot.motors.stop_all_motors()
        if (sensor < 200 ):
            print(counter)
            robot.behavior.turn_in_place(degrees(-90))
            counter = counter + 1
        if (sensor >= 200 and counter != 0):
            robot.behavior.drive_straight(distance_mm(200), speed_mmps(200))
            robot.behavior.turn_in_place(degrees(90))
            print(counter)
            if (sensor < 200):
                robot.behavior.turn_in_place(degrees(-90))
                print(counter)
            else:
                counter = counter - 1

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
    return ""
