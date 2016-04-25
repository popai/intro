import RPi.GPIO as GPIO
from webPI import app
from flask import render_template, session, url_for, redirect
from webPI.models import User, db 
import time

# Grab all pins from the configuration file
PINS = {
        18 : {'name' : 'Iesire 1', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        25 : {'name' : 'Iesire 4', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        23 : {'name' : 'Iesire 2', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        24 : {'name' : 'Iesire 3', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        17 : {'name' : 'Intrare 0', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        21 : {'name' : 'Intrare 1', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        7 : {'name' : 'Test LED', 'state' : '', 'type' : 'test', 'time' : int(time.time()), 'msg' : True}
        }
    
    
pins = PINS  

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

d = {1:0, 0:1}
    
# Set each pin as table defined an output and make it low
for pin in pins: 
    if pins[pin]['type'] != "input":
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    pins[pin]['state'] = 0
    else: 
        GPIO.setup(pin, GPIO.IN)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
 
    #user = User().query.filter_by(email = session['email']).first()
    user = db.session().query(User).filter_by(email = session['email']).first()
        
    if user is None:
        return redirect(url_for('signin'))
    else:
        for pin in pins:
	        #if pins[pin]['type'] == "input":	    		
            pins[pin]['state'] = GPIO.input(pin)
    
            # Put the pin dictionary into the template data dictionary
            templateData = {
                        'pins' : pins
                    }
        return render_template('profile.html', **templateData)


# The function below is executed when someone requests a URL without a
# pin number -> master control for all pins
@app.route('/profile/<master>')
def master(master):
    if 'email' not in session:
        return redirect(url_for('signin'))
 
    #user = User().query.filter_by(email = session['email']).first()
    user = db.session().query(User).filter_by(email = session['email']).first()
        
    if user is None:
        return redirect(url_for('signin'))

    if master == 'on':
        # Set all pins to high
        for pin in pins:
            if pins[pin]['type'] != "input":
                GPIO.output(pin, GPIO.HIGH)
                pins[pin]['state'] = GPIO.input(pin)
                
            time.sleep(0.02)
            pins[pin]['time'] = int(time.time())
           
        message = 'Turned all interfaces on.'
    if master == 'off':
        # Set all pins to low
        for pin in pins:
            if pins[pin]['type'] != "input":
                GPIO.output(pin, GPIO.LOW)
                pins[pin]['state'] = GPIO.input(pin)
                
        message = 'Turned all interfaces off.'
        
    # For each pin, read the pin state and store it in the pins dictionary
    for pin in pins:
	    #if pins[pin]['type'] == "input":
        pins[pin]['state'] = GPIO.input(pin)
        
    # Along with the pin dictionary, put the message into the template data dictionary
    templateData = {
                    'message' : message,
                    'pins' : pins
                    }
    #app.root_path = 'profile'
    return render_template('profile.html', **templateData)

# The function below is executed when someone requests a URL with the
# pin number and action in it
@app.route('/profile/<changePin>/<action>')
def action(changePin, action):
    if 'email' not in session:
        return redirect(url_for('signin'))
 
    #user = User().query.filter_by(email = session['email']).first()
    user = db.session().query(User).filter_by(email = session['email']).first()
        
    if user is None:
        return redirect(url_for('signin'))

    # Convert the pin from the URL into an integer
    changePin = int(changePin)
    # Get the device name for the pin being changed
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below
    if action == 'on':
        # Set the pin high
        GPIO.output(changePin, GPIO.HIGH)
        pins[changePin]['time'] = int(time.time())
        pins[changePin]['state'] = GPIO.input(pin)        
        # Save the status message to be passed into the template
        message = 'Turned ' + deviceName + ' on.'
        
    if action == 'off':
        GPIO.output(changePin, GPIO.LOW)
        pins[changePin]['state'] = GPIO.input(pin)
        # Save the status message to be passed into the template
        message = 'Turned ' + deviceName + ' off.'
        
    if action == 'toggle':
        # Read the pin and set it to whatever it isn't (that is, toggle it)
        #GPIO.output(changePin, not pins[changePin]['state'])
        GPIO.output(changePin, not GPIO.input(changePin))
        #pins[changePin]['state'] = d[pins[changePin]['state']]
        # Save the status message to be passed into the template
        message = 'Toggled ' + deviceName + '.'
        
    if action == 'reset':
        # Set the pin to low and after 5 s back to high
        GPIO.output(changePin, GPIO.LOW)
        time.sleep(5)
        GPIO.output(changePin, GPIO.HIGH)
        pins[changePin]['time'] = int(time.time())
	    pins[changePin]['state'] = GPIO.input(changePin)
        # Save the status message to be passed into the template
        message = 'Reset ' + deviceName + '.'
        
    # For each pin, read the pin state and store it in the pins dictionary
    for pin in pins:
	   #if pins[pin]['type'] == "input":
        pins[pin]['state'] = GPIO.input(pin)
        
    templateData = {
                    'message' : message,
                    'pins' : pins
                    }
    #app.root_path = 'profile'
    return render_template('profile.html', **templateData)

def offPin():
    while 1:
        stopTime = int(time.time())
        for pin in pins:
            #print(pins[pin]['time'])
            if pins[pin]['type'] != "input" and pins[pin]['state']:
                startTime = pins[pin]['time']
                if (stopTime - startTime) > 60:
                    print("pin OFF")
                    GPIO.output(pin, GPIO.LOW)
                    pins[pin]['state'] = GPIO.input(pin)
                    
                    
        time.sleep(10)
