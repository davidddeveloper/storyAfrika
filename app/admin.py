from django.contrib import admin
from .schema import Profile, Story, Topic, Comment

# Register your models here.
admin.site.register(Story)
admin.site.register(Topic)
admin.site.register(Comment)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'get_email', 'short_bio', 'about', 'avatar', 'banner', 'registration_finish')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Optional: to customize the column header

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'  # Optional: to customize the column header