import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'SOME RANDOM VALUE'
    WTF_CSRF_ENABLED = False
