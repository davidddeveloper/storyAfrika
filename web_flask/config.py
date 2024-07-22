import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'SOME RANDOM VALUE'
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_DOMAIN = 'localhost'
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = False
    # FOR FILE UPLOAD
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png']
    UPLOAD_PATH = 'static/uploads'
