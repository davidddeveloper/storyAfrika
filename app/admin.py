from django.contrib import admin
from .schema import Profile, Story, Topic, Comment

# Register your models here.
admin.site.register(Story)
admin.site.register(Topic)
admin.site.register(Comment)

admin.site.register(Profile)