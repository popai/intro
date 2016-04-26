#!/usr/bin/env python
import os
from webPI import app
from flask import render_template, request, flash, session, url_for, redirect
from webPI.forms import ContactForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from webPI.models import User, db, build_sample_db
#from flask_bootstrap import Bootstrap

import threading, time
import webPI.pinsAction


mail = Mail(app)
#Bootstrap(app)

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
        for pin in webPI.pinsAction.pins:
            #if webPI.pinsAction.pins[pin]['type'] == 'output':
                if webPI.pinsAction.pins[pin]['state'] == 1 and webPI.pinsAction.pins[pin]['type'] == 'input':
                    if webPI.pinsAction.pins[pin]['msg']:
                        webPI.pinsAction.pins[pin]['msg'] = False
                        deviceName = webPI.pinsAction.pins[pin]['name']
                        message = deviceName + " ON"
                        print(message)
                        send_email('rpi.webc@gmail.com', '2016Marti03', 'cretu_dan2003@yahoo.com', 'pi alert', message)

                else:
                    if webPI.pinsAction.pins[pin]['msg'] == False:
                        deviceName = webPI.pinsAction.pins[pin]['name']
                        message = deviceName + " OFF"
                        print(message)
                        send_email('rpi.webc@gmail.com', '2016Marti03', 'cretu_dan2003@yahoo.com', 'pi alert', message)
                    webPI.pinsAction.pins[pin]['msg'] = True

        time.sleep(0.2)
           
t1 = threading.Thread(target=inPins)
t1.start()

t2 = threading.Thread(target=webPI.pinsAction.offPin)
t2.start()                    

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    app.run(host='0.0.0.0', port=5000, debug=False)

    #app.run(debug=False)
