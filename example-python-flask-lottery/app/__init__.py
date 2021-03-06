from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from celery import Celery	
from celery.decorators import periodic_task
from datetime import timedelta
from celery.task.schedules import crontab
from app.data import db
from flask.ext.login import LoginManager


app = Flask(__name__)
app.logger.debug("")

app.config.from_object('config')

#Bootstrap extension
Bootstrap(app)

#Login manager
login_manager = LoginManager()
login_manager.init_app(app)

#Build the database:
#This will create the database file using SQLAlchemy
db.init_app(app)
db.app = app
db.create_all()


from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_winners.controllers import mod_winner as winner_module

app.register_blueprint(auth_module)
app.register_blueprint(winner_module)
#Add more module if ti is necessary
from app.mod_auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




#email logger
from config import basedir, ADMINS,MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
if not app.debug:
	import logging
	from logging.handlers import SMPTHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials = (MAIL_USERNAME, MAIL_PASSWORD)
	mail_handler = SMTPHandler((MAIL_SERVER,MAIL_PORT),'no-reply@'+MAIL_SERVER,ADMINS, 'app failure',credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/app.log','a',1*1024*1024,10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('app startup')


