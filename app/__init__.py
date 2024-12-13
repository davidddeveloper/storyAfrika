from helpers import ImageUpload

from django.conf import settings

image_upload = ImageUpload(settings.cloud_name, settings.api_key, settings.api_secret)