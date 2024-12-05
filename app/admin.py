from django.contrib import admin
from .schema import Profile, Story, Topic, Comment, StoryImage

# Register your models here.

common_field = ['id', 'created_at', 'updated_at']

class StoryImageInline(admin.TabularInline):  # or admin.StackedInline for a different style
    model = StoryImage
    extra = 1  # Number of empty image upload slots displayed

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    inlines = [StoryImageInline]
    list_display = ('title', 'writer', 'status')
    exclude = common_field + [ 'likes', ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    exclude = common_field + ['followers']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'commenter', 'story')
    exclude = common_field + ['likes', 'unlikes']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'get_email', 'short_bio', 'about', 'avatar', 'banner', 'registration_finish')
    exclude = common_field + ['user', 'followers']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Optional: to customize the column header

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'  # Optional: to customize the column header


