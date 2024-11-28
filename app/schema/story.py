from django.db import models
from .base_model import Base

STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}

class Story(Base):
    """ Represents a story
    """
    
    title = models.CharField(max_length=200, null=False)
    text = models.TextField(max_length=5000, null=False)
    writer = models.ForeignKey(to='Profile', on_delete=models.CASCADE, null=False, related_name='stories')
    topics = models.ManyToManyField(to='Topic', blank=True, related_name='stories')

    contributors = models.ManyToManyField(to='Profile', blank=True, related_name='stories_contributed_to')

    likes = models.ManyToManyField(to='Profile', blank=True, related_name='likers')

    image = models.ImageField(upload_to='media/', null=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d")

    def __str__(self):
        return self.title