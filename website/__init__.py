import os
import threading
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

DB_NAME = "database.db"

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
   
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    from .views import views
    from .auth import auth
    from .models import User
    from .utils import schedule_email_job, start_scheduler

    app.register_blueprint(views, url_prefix='/')   
    app.register_blueprint(auth, url_prefix='/auth')


    with app.app_context():
        db.create_all()
        schedule_email_job()


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    try:
        scheduler_thread = threading.Thread(target=start_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    except Exception as e:
        print(f"Error starting scheduler: {e}")

    return app


def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        print('Creating Database....')
        with app.app_context():
            db.create_all()
        

    

    