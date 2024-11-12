from flask import Flask, redirect, url_for
from humanize_number.humanize_flask import init_app
from flask_login import LoginManager, current_user
from models.engine import storage
from web_flask.config import Config
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_cors import CORS
#from flask_mail import Mail, Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from .helpers.complete_registration import complete_registration

app = Flask(__name__)
init_app(app)
# app.config['SECRET_KEY'] = 'SOME RANDOM VALUE'
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
#CSRFProtect(app)
#Session(app)
# mail
mail = Mail(app)


def send_welcome_email(user_email, first_name):
    with app.app_context():
        subject = "Welcome to StoryAfrika!"
        body = f"""
        Hi {first_name},

        Welcome to StoryAfrika! We’re excited to have you join our community. Here at StoryAfrika, we share inspiring stories from across Africa, focusing on success stories and the journeys behind them. From entrepreneurs and artists to everyday heroes, we cover how they achieved their goals and overcame challenges.

        With StoryAfrika, you can:
        - Read stories that motivate and inspire.
        - Share your own success stories or journeys.
        - Connect with a community of like-minded individuals.

        We hope you enjoy your journey with us and look forward to your contributions and engagement!

        Best Regards,
        The StoryAfrika Team
        """

        #msg = Message(subject, recipients=[user_email])
        #msg.body = body
        #mail.send(msg)

        message = Mail(
            from_email=('storyafrika.live@gmail.com', 'StoryAfrika Team'),
            to_emails=user_email,
            subject=subject,
            plain_text_content=body
        )

        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending email: {e}")

from web_flask.app import routes
