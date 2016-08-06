import RPi.GPIO as GPIO
from webPI import app
from flask import render_template, session, url_for, redirect
from models import User, db 
import time

# Grab all pins from the configuration file
PINS = {
    0 : {'name' : 'Program Aspersoare', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True}, 
        2 : {'name' : 'HIDROFOR', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        3 : {'name' : 'GAZON ZONA 1', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        4 : {'name' : 'GAZON ZONA 2', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        5: {'name' : 'GAZON ZONA 3', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        6 : {'name' : 'GAZON ZONA 4', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        9 : {'name' : 'GAZON ZONA 5', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        10 : {'name' : 'GAZON ZONA 6', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        11 : {'name' : 'Iesire 7', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        13 : {'name' : 'Iesire 8', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        17 : {'name' : 'Iesire 9', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        19 : {'name' : 'Iesire 10', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        22 : {'name' : 'SIRENA', 'state' : '', 'type' : 'output', 'time' : int(time.time()), 'msg' : True},
        7: {'name' : 'PANICA ALARMA', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        12: {'name' : 'Intrare 2', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        16: {'name' : 'Intrare 3', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        20 : {'name' : 'Intrare 4', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True},
        21 : {'name' : 'NIVEL APA SCAZUTA', 'state' : '', 'type' : 'input', 'time' : int(time.time()), 'msg' : True}
        }    

pins = PINS  

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#d = {1:0, 0:1}
    
# Set each pin as table defined an output and make it low
for pin in pins: 
    if pins[pin]['type'] == "output":
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        pins[pin]['state'] = 1
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
                GPIO.output(pin, GPIO.LOW)
                pins[pin]['state'] = GPIO.input(pin)
                
            time.sleep(0.02)
            pins[pin]['time'] = int(time.time())
           
        message = 'Turned all interfaces on.'
    if master == 'off':
        # Set all pins to low
        for pin in pins:
            if pins[pin]['type'] != "input":
                GPIO.output(pin, GPIO.HIGH)
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
    #return render_template('profile.html', **templateData)
    return redirect(url_for('profile'))

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
        GPIO.output(changePin, GPIO.LOW)
        pins[changePin]['time'] = int(time.time())
        pins[changePin]['state'] = GPIO.input(changePin)        
        # Save the status message to be passed into the template
        message = 'Turned ' + deviceName + ' on.'
        
    if action == 'off':
        GPIO.output(changePin, GPIO.HIGH)
        pins[changePin]['state'] = GPIO.input(changePin)
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
        GPIO.output(changePin, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(changePin, GPIO.LOW)
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
    #return render_template('profile.html', **templateData)
    return redirect(url_for('profile'))

def progAsp():
    timeSleap = 3660 #1 ora si 2 min
    while 1:
        if not pins[0]['state']:
            pins[0]['time'] = int(time.time()) + 18300  #prog port
            
        GPIO.output(2, GPIO.LOW)
            pins[2]['state'] = GPIO.input(2)                #HIDROFOR
            pins[2]['time'] = int(time.time()) + 18300
            
            if not pins[0]['state']:
        GPIO.output(3, GPIO.LOW)
                pins[3]['state'] = GPIO.input(3)
                pins[3]['time'] = int(time.time())
                time.sleep(timeSleap)
            
            if not pins[0]['state']:
        GPIO.output(4, GPIO.LOW)
                pins[4]['state'] = GPIO.input(4)
                pins[4]['time'] = int(time.time())
                time.sleep(timeSleap)
                
            if not pins[0]['state']:
        GPIO.output(5, GPIO.LOW)
                pins[5]['state'] = GPIO.input(5)
                pins[5]['time'] = int(time.time())
                #GPIO.output(7, GPIO.LOW)
                time.sleep(timeSleap)
    
            if not pins[0]['state']:
        GPIO.output(6, GPIO.LOW)
                pins[6]['state'] = GPIO.input(6)
                pins[6]['time'] = int(time.time())
                #GPIO.output(8, GPIO.LOW)
                time.sleep(timeSleap)
                
            if not pins[0]['state']:
        GPIO.output(9, GPIO.LOW)
                pins[9]['state'] = GPIO.input(9)
                pins[9]['time'] = int(time.time())
                #GPIO.output(9, GPIO.LOW)
                time.sleep(timeSleap)

        GPIO.output(3, GPIO.HIGH)
            pins[3]['state'] = GPIO.input(3)

        GPIO.output(4, GPIO.HIGH)
            pins[4]['state'] = GPIO.input(4)

        GPIO.output(5, GPIO.HIGH)
            pins[5]['state'] = GPIO.input(5)

        GPIO.output(6, GPIO.HIGH)
            pins[6]['state'] = GPIO.input(6)

        GPIO.output(9, GPIO.HIGH)
            pins[9]['state'] = GPIO.input(9)
                
        GPIO.output(0, GPIO.HIGH)
            pins[0]['state'] = GPIO.input(0)
        GPIO.output(2, GPIO.HIGH)
            pins[2]['state'] = GPIO.input(2)
            
            
        time.sleep(10)
    


def offPin():
    while 1:
        stopTime = int(time.time())
        for pin in pins:
            if pins[pin]['type'] != "input" and pins[pin]['state'] == 0:
                startTime = pins[pin]['time']
                if (stopTime - startTime) > 3600:
                    print("pin OFF")
                    GPIO.output(pin, GPIO.HIGH)
                    pins[pin]['state'] = GPIO.input(pin)                   
                    
        time.sleep(60)
    #time.sleep(10)

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

def inPins():
    #import smtplib

    while 1:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
         
            if pins[pin]['msg'] == True:
                    if pins[pin]['state'] == 0:
                        message = pins[pin]['name'] + " ON"
                        pins[pin]['msg'] = False
                        print(message)
                        #send_email('popai307@gmail.com', 'maistrul', 'popai@b.astral.ro', 'intrari', message)
            send_email('rpi.webc@gmail.com', '2016Marti03', 'cretu_dan2003@yahoo.com', 'pi alert', message)
                        
            else:
                    if pins[pin]['state'] == 1:
                        message = pins[pin]['name'] + " OFF"
                        pins[pin]['msg'] = True
                        print(message)
                        #send_email('popai307@gmail.com', 'maistrul', 'popai@b.astral.ro', 'intrari', message)
            send_email('rpi.webc@gmail.com', '2016Marti03', 'cretu_dan2003@yahoo.com', 'pi alert', message)
                         
        time.sleep(0.2)
