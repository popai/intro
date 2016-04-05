from flask import Flask


app = Flask(__name__)
 
#app = Flask(__name__)
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'popai307@gmail.com'
app.config["MAIL_PASSWORD"] = 'maistrul'

#import webA.webControl 
#from routes import mail
#mail.init_app(app)

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = False
 
#from models import db
#db.init_app(app)