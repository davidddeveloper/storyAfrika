from django.db import models
from tinymce.models import HTMLField
from .story import Story

STATUS = (
    ('a', 'Active'),
    ('i', 'Inactive')
)
class FeaturingStory(models.Model):
    caption = models.CharField(null=False, max_length=50)
    banner = models.ImageField(upload_to="media/", null=False, default='something')
    story = models.ForeignKey(to=Story, null=False, related_name='has_featured', on_delete=models.CASCADE)
    intro_to_story = HTMLField()
    status = models.CharField(max_length=1, choices=STATUS, default="a")

    def __str__(self):
        return self.caption
