#import RPi.GPIO as GPIO
from webA import app
from flask import render_template, session, url_for, redirect
from webA.models import User, db 
import time

# Grab all pins from the configuration file
PINS = {
        17 : {'name' : 'Interface 0', 'state' : '', 'type' : 'production'},
        27 : {'name' : 'Interface 1', 'state' : '', 'type' : 'production'},
        23 : {'name' : 'Interface 2', 'state' : '', 'type' : 'production'},
        24 : {'name' : 'Interface 3', 'state' : '', 'type' : 'production'},
        7 : {'name' : 'Test LED', 'state' : '', 'type' : 'test'}
        }
    
    
pins = PINS  
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

    
# Set each pin as an output and make it low
#for pin in pins:
    #GPIO.setup(pin, GPIO.OUT)
    #GPIO.output(pin, GPIO.LOW)

@app.route('/profile')
def pisState():
    if 'email' not in session:
        return redirect(url_for('signin'))
 
    #user = User().query.filter_by(email = session['email']).first()
    user = db.session().query(User).filter_by(email = session['email']).first()
        
    if user is None:
        return redirect(url_for('signin'))
    # For each pin, read the pin state and store it in the pins dictionary
    for pin in pins:
        pins[pin]['state'] = 'ceva'#GPIO.input(pin)
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
        #for pin in pins:
            #GPIO.output(pin, GPIO.HIGH)
        message = 'Turned all interfaces on.'
    if master == 'off':
        # Set all pins to low
        #for pin in pins:
            #GPIO.output(pin, GPIO.LOW)
        message = 'Turned all interfaces off.'
    # For each pin, read the pin state and store it in the pins dictionary
    for pin in pins:
        pins[pin]['state'] = 'test'#GPIO.input(pin)
        # Along with the pin dictionary, put the message into the template data dictionary
    templateData = {
                    'message' : message,
                    'pins' : pins
                    }
    app.root_path = 'profile'
    return render_template('profile.html', **templateData)
    #return redirect(url_for('profile'))

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
        #GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template
        message = 'Turned ' + deviceName + ' on.'
    if action == 'off':
        #GPIO.output(changePin, GPIO.LOW)
        message = 'Turned ' + deviceName + ' off.'
    if action == 'toggle':
        # Read the pin and set it to whatever it isn't (that is, toggle it)
        #GPIO.output(changePin, not GPIO.input(changePin))
        message = 'Toggled ' + deviceName + '.'
    if action == 'reset':
        # Set the pin to low and after 5 s back to high
        #GPIO.output(changePin, GPIO.LOW)
        time.sleep(5)
        #GPIO.output(changePin, GPIO.HIGH)
        message = 'Reset ' + deviceName + '.'
    # For each pin, read the pin state and store it in the pins dictionary
    #for pin in pins:
        #pins[pin]['state'] = GPIO.input(pin)
    templateData = {
                    'message' : message,
                    'pins' : pins
                    }
    app.root_path = 'profile'
    return render_template('profile.html', **templateData)



