"""
    cloudinary_image_upload.py: base class to upload images to cloudinary
"""
import os
from werkzeug.utils import secure_filename
from cloudinary import config
from cloudinary import uploader

class ImageUpload:
    """Represent ImageUpload"""

    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.gif', '.svg', '.webp', '.heic', '.heif', '.jfif']

    def __init__(self, cloud_name, api_key, api_secret):
        config(
            cloud_name = cloud_name,
            api_key = api_key,
            api_secret = api_secret
        )

    def upload(self, file, user_id):
        """ Upload to cloudinary """
        # self.validate(file)
        result = uploader.upload(file, folder=user_id)
        return {"image_url": result['secure_url']}

    def validate(file):
        """ Validate file extension and performs other security checks """
        if not file:
            raise ValueError("No file passed")

        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in ImageUpload.UPLOAD_EXTENSIONS:
            raise TypeError("File not accepted")
