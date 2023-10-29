from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField, PasswordField, BooleanField, ValidationError,
                     DateTimeField, TextAreaField, SelectField, DateTimeLocalField)
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp, InputRequired
from webapp.models import User, TaskCategory


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(
        '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=5, max=20, message="Please provide a valid name")])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=15)])
    password_confirm = PasswordField('Password Confirm', validators=[
                                     InputRequired(), EqualTo('password', message="Passwords must match !")])
    submit = SubmitField('submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp(
        '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateTimeLocalField('Due Date', validators=[InputRequired()], format="%Y-%m-%dT%H:%M")
    status = BooleanField('Status')
    priority = SelectField('Priority', choices=[(
        "low", "Low"), ("medium", "Medium"), ("high", "High")])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddTaskCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
                                 InputRequired(), Length(min=8, max=15)])
    new_password = PasswordField('New Password', validators=[
                                 InputRequired(), Length(min=8, max=15)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     InputRequired(), EqualTo('new_password', message="Passwords must match !")])
    submit = SubmitField('Submit')