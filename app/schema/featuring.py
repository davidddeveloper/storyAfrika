from django.db import models
from .story import Story

STATUS = (
    ('a', 'Active'),
    ('i', 'Inactive')
)
class FeaturingStory(models.Model):
    caption = models.CharField(null=False, max_length=50)
    image = models.ImageField(null=False)
    story = models.ForeignKey(to=Story, null=False, related_name='has_featured', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default="a")
