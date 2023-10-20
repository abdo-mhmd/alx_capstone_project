from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager


db_config = {
    'host': 'localhost',
    'user': 'root',
    'pass': 'root',
    'database': 'taskmanagerdb',
    'port': 3306
}

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

login_manager.login_view = "login"
login_manager.session_protection = "strong"
def create_database(app):
    with app.app_context():
        db.create_all()
        db.session.commit()


def create_app():
    app = Flask(__name__)

    # Set the secret key for your application
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'\
        .format(db_config['user'],
                db_config['pass'],
                db_config['host'],
                db_config['port'],
                db_config['database'])
    
    login_manager.init_app(app)

    db.init_app(app)
    create_database(app)
    bcrypt.init_app(app)

    migrate.init_app(app, db)

    return app
