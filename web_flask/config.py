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
