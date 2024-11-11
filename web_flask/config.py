import os
import redis


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'SOME RANDOM VALUE'
    #SESSION_COOKIE_NAME = 'mysession'
    SESSION_COOKIE_DOMAIN = 'stories.storyafrika.live'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = False
    # I'm going to go with redis in production on ubuntu server
    #SESSION_TYPE = 'redis'
    #SESSION_PERMANENT = False
    #SESSION_USE_SIGNER = True
    #SESSION_REDIS = redis.from_url('redis://localhost:6379')
    # FOR FILE UPLOAD
    MAX_CONTENT_LENGTH = 40 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.gif', '.svg', '.webp', '.heif', '.heic', '.jfif']
    UPLOAD_PATH = os.path.join(os.path.dirname(__file__), '..', 'uploads')

    # login or signup with google
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

    # flask mail
    MAIL_SERVER = 'smtp.gmail.com'  # e.g., 'smtp.gmail.com'
    MAIL_PORT = 587  # or 465 for SSL
    MAIL_USE_TLS = True  # Use TLS for security
    MAIL_USE_SSL = False  # Set to True if using SSL
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('StoryAfrika Team', os.getenv('MAIL_USERNAME'))