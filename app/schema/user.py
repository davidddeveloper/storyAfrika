from django.db import models
from django.contrib.auth.models import User
from .base_model import Base

class Profile(Base):
    """
        Represents a user

        Attributes:
            - username: user identity on the platform
            - fullname: first name last name and any other name
            - email: user email address
            - password: password of the user
            - short_bio: who the user is
            - about: detail description of the user
    """
    from app.schema.story import Story

    user = models.OneToOneField(to=User, null=False, on_delete=models.CASCADE)
    short_bio= models.CharField(max_length=160, null=True, blank=True)
    about = models.TextField(max_length=500, null=True, blank=True)
    # full_name = models.CharField(max_length=50, null=True, default=(first_name + ' ' + last_name))

    avatar = models.CharField(max_length=200, null=True, blank=True)
    banner = models.CharField(max_length=200, null=True, blank=True, default='https://fastly.picsum.photos/id/91/800/500.jpg?hmac=J_kCOn2MZlDuJIb_rU14DYnb6HMv55ynWirbSF9l8f0')
    registration_finish = models.BooleanField(default=False)

    followers = models.ManyToManyField(to='Profile', blank=True, related_name='following')

    bookmarks = models.ManyToManyField(to=Story, blank=True, related_name="bookmarkers")

    def __str__(self):
        return f'{self.user.username}'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)