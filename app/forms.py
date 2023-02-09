from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import EqualTo, InputRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()

class ColorForm(FlaskForm):
    color = StringField('Color', validators=[InputRequired()])
    submit = SubmitField()

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    body = StringField('Entry', validators=[InputRequired()])
    submit = SubmitField()