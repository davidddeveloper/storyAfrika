"""
Django settings for storyafrika project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # load environments variables from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'storyafrika.live', 'www.storyafrika.live', '51.124.245.236']

# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ckeditor_uploader',
    'tinymce',
    'hitcount',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'storyafrika.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storyafrika.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',

        # mysql
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'storyafrika',
        "USER": os.getenv('MYSQL_USER'),
        "PASSWORD": os.getenv('MYSQL_PASSWORD'),
        "HOST": 'localhost',
        "PORT": 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

MEDIA_ROOT = Path(BASE_DIR, 'images')
MEDIA_URL = 'media/'

STATICFILES_DIRS = [
    Path(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# sending emails
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SENDGRID_API_KEY = os.getenv('# ')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'storyafrika@mail.storyafrika.live'

CORS_ALLOWED_ORIGINS = [
    "https://storyafrika.live",
    "https://51.124.245.236",
    "https://51.124.245.236:443",

]

CSRF_TRUSTED_ORIGINS = [
    "https://storyafrika.live",
    "http://127.0.0.1:8000"
    "https://51.124.245.236",
    "https://51.124.245.236:443"
]


# Allow specific methods if needed
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Optional: Allow any headers if needed
CORS_ALLOW_HEADERS = ['*']


# CKEDITOR SETTINGS
CKEDITOR_UPLOAD_PATH = 'media/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 'auto',
        'extraPlugins': ','.join(['image2']),  # Enable additional plugins like image handling
    },
}


TINYMCE_DEFAULT_CONFIG = {
    'script_url': '/static/js/tinymce_hacks.js',
    "height": 500,
    "width": "auto",
    "menubar": "file edit view insert format tools table help",
    "plugins": "autosave advlist autolink lists link image charmap print preview anchor "
               "searchreplace visualblocks code fullscreen "
               "insertdatetime media table paste code help wordcount",
    "toolbar": "undo redo |  cut custom_copy custom_paste formatselect | bold italic underline backcolor | "
               "alignleft aligncenter alignright alignjustify | "
               "bullist numlist outdent indent | removeformat | help",
    "paste_as_text": True,  # Ensures pasted content is clean
    # "mobile": {
    #     "plugins": "autosave lists autolink paste table code wordcount help",
    #     "toolbar": "undo redo |  cut custom_copy custom_paste bold italic underline | bullist numlist |"
    # },
    "contextmenu": "link custom_copy custom_paste",
    "browser_spellcheck": True,  # Enable browser spellcheck for better UX
    "paste_data_images": True,

    # copy / paste fixing
    'paste_as_text': True,
    'clipboard_append': True,
    'clipboard_paste_before': True,
    'setup': 'function(editor) { editor.ui.registry.addButton("custom_copy", { text: "Copy", onAction: function() { navigator.clipboard.writeText(editor.getContent()); } }); editor.ui.registry.addButton("custom_paste", { text: "Paste", onAction: function() { navigator.clipboard.readText().then(function(text) { editor.execCommand("mceInsertContent", false, text); }); } }); }',
    
    'permission': 'clipboard-read',
}


# CLOUDINARY SETTINGS
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY = {
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET'),
}

cloudinary.config(
    cloud_name=CLOUDINARY['cloud_name'],
    api_key=CLOUDINARY['api_key'],
    api_secret=CLOUDINARY['api_secret'],
)
