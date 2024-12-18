from django.contrib import admin

@admin.action(description='Publish Selected Stories')
def publish_stories(modeladmin, request, queryset):
    queryset.update(status='p')

@admin.action(description='Withdraw Selected Stories')
def withdraw_stories(modeladmin, request, queryset):
    queryset.update(status='w')

@admin.action(description='Draft Selected Stories')
def draft_stories(modeladmin, request, queryset):
    queryset.update(status='d')