from werkzeug import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from webPI import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))
   
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
     
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)



def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    #import string
    #import random

    db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    #test_user = User(login="test", password=generate_password_hash("test"))
    #db.session.add(test_user)

    user = User('admin','admin','admin@gmail.com','admin')
    db.session.add(user)
    db.session.commit()
    return
"""   
    for i in range(len(first_names)):
        #user = User('test', 'test','test','test')
        user.firstname = first_names[i]
        user.lastname = last_names[i]
        #user.login = user.first_name.lower()
        #user.email = user.login + "@example.com"
        user.email = user.firstname + "@example.com"
        user.pwdhash = "test"
        #db.app.add(user)
        db.session.add(user)
"""
    
    


 
    
# Create user model.
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
"""
