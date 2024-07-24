#!/usr/bin/python3
""" This module represents methods and classes for image upload

"""
from flask_login import current_user
from flask import abort, send_from_directory
from werkzeug.utils import secure_filename
import os
import imghdr

UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.gif', '.svg', '.webp']
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), '..', 'uploads')



class ImageUpload:
    """ Represents images """

    def validate_image(stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')

    def image_upload(self, file):
        filename = secure_filename(file.filename)
        if filename:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in UPLOAD_EXTENSIONS:
                raise ValueError("File extension not acceptable")
            if file_ext != ImageUpload.validate_image(file.stream):
                raise ValueError("Invalid image format")
            
            upload_dir = os.path.join(UPLOAD_PATH, current_user.get_id())
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
        
            return filename
        return None