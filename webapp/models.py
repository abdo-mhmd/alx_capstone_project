from webapp import db as database
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, database.Model):
    """Represents a user in the system."""

    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, index=True)
    username = database.Column(database.String(64), unique=True, index=True)
    password = database.Column(database.String(128))
    authenticated = database.Column(database.Boolean, default=False)
    tasks = database.relationship('Task', backref='task', lazy='dynamic')

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
    def __repr__(self):
        return '<User %r>' % self.username

class TaskCategory(database.Model):
    """Represents a category of tasks in the system."""

    __tablename__ = 'taskcategories'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), nullable=False)
    tasks = database.relationship('Task', backref='taskcategory', lazy='dynamic')


class Task(database.Model):
    """Represents a task in the system."""

    __tablename__ = 'tasks'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(64), nullable=False)
    description = database.Column(database.String(256))
    status = database.Column(database.Boolean, default=False)
    priority = database.Column(database.String(20))
    due_date = database.Column(database.DateTime, default=datetime.now())
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('taskcategories.id'), nullable=False)
    categories = database.relationship("TaskCategory", foreign_keys=[category_id])



