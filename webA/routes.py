import os
from webA import app
from flask import render_template, request, flash, session, url_for, redirect
from webA.forms import ContactForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from webA.models import User, db, build_sample_db
from flask_bootstrap import Bootstrap

import threading, time
import webA.pinsAction


mail = Mail(app)
Bootstrap(app)
"""
@app.route('/')
def home():
    return render_template('home.html')
"""
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['popai@b.astral.ro'])
            msg.body = """From: %s <%s> %s""" %(form.name.data, form.email.data, form.message.data) 
            mail.send(msg)
            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if 'email' not in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session().add(newuser)
            db.session().commit()
                   
            session['email'] = newuser.email
       
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
   
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))
                 
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
     
    session.pop('email', None)
    return redirect(url_for('signin'))


def inPins():
    while 1:
        for pin in webA.pinsAction.pins:
            if webA.pinsAction.pins[pin]['type'] == 'output':
                if webA.pinsAction.pins[pin]['state'] == 0:
                    if webA.pinsAction.pins[pin]['msg']:
                        webA.pinsAction.pins[pin]['msg'] = False
                        deviceName = webA.pinsAction.pins[pin]['name']
                        message =    deviceName + " OFF"
                        print(message)
                        mesg = Message(deviceName, sender='popai307@gmail.com', recipients=['popai@b.astral.ro'])
                        mesg.body = message #"""From: %s <%s> %s""" %(deviceName, 'popai@b.astral.ro', message) 
                        mail.send(mesg)
                else:
                    if webA.pinsAction.pins[pin]['msg'] == False:
                        deviceName = webA.pinsAction.pins[pin]['name']
                        message = deviceName + " ON"
                        print(message)
                        #msg = Message(deviceName, sender='contact@example.com', recipients=['popai@b.astral.ro'])
                        #msg.body = From: %s <%s> %s %(deviceName, session['email'], message) 
                        #mail.send(msg)
                    webA.pinsAction.pins[pin]['msg'] = True
        time.sleep(2)
           
t1 = threading.Thread(target=inPins)
t1.start()

t2 = threading.Thread(target=webA.pinsAction.offPin)
t2.start()                    

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    #app.run(host='192.168.0.12', port=80, debug=True)

    app.run()
