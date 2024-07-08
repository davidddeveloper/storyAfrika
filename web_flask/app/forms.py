"""
    forms: wtf forms
"""
import os
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from web_flask.app import storage
from models.user import User


class LoginForm(FlaskForm):
    """ Represent a login form """
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')


class UserRegistrationForm(FlaskForm):
    """ Represent a form to register a new user """
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = storage._session.query(User).where(
                User.username == username.data
            ).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        if os.getenv('STORAGE') in ['db', 'DB']:
            user = storage._session.query(User).where(
                    User.email == email.data
                ).first()

            if user is not None:
                raise ValidationError('Please use a different email address')

        else:  # file_storage
            pass  # do nothing for now
