import os

if os.getenv('IMAGE_UPLOAD_TYPE') == 'local':
    from models.image_upload import ImageUpload
    image_upload = ImageUpload()

if os.getenv('IMAGE_UPLOAD_TYPE') == 'cloud':
    from models.cloudinary_image_upload import ImageUpload

    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')

    image_upload = ImageUpload(cloud_name, api_key, api_secret)
