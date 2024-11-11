"""
    forms: wtf forms
"""
import os
from flask_login import current_user
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
        if current_user.is_authenticated:
            if user is not None and user != current_user:  # user is not current and user with that email exists:
                raise ValidationError('Please use a different username')
        else:
            if user is not None:
                raise ValidationError('Please use a different username')

    def validate_email(self, email):
        if os.getenv('STORAGE') in ['db', 'DB']:
            user = storage._session.query(User).where(
                    User.email == email.data
                ).first()

            # this seem stupid but I'm doing this because
            # i'm reusing this in the login user page
            if current_user.is_authenticated:
                if user is not None and user != current_user:  # user is not current and user with that email exists
                    raise ValidationError('Please use the same email address')
            else:
                if user is not None:
                    raise ValidationError('Please use a different email address')

        else:  # file_storage
            pass  # do nothing for now


class UserUpdateForm(UserRegistrationForm, FlaskForm):
    """ Represents a form to update the user model """

    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    short_bio = StringField('Short Bio', validators=[])
    about = StringField('About', validators=[])
    username = StringField('Username', validators=[])
    email = EmailField('Email', validators=[Email()])
    current_password = PasswordField('Current Password', validators=[])
    new_password = PasswordField(
        'New Password', validators=[]
    )
    password = None
    password2 = None
    submit = SubmitField('Update')

    def validate_current_password(self, current_password):
        if current_password.data and not current_user.check_password(current_password.data):
            raise ValidationError('Password Incorrect')