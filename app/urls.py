from django.urls import path
from .views import first_home_page, sign_in, sign_out, join_us, story

app_name = 'app'

urlpatterns = [
    path('', view=first_home_page, name='home'),
    path('sign_in', view=sign_in, name='sign_in'),
    path('sign_out', view=sign_out, name='sign_out'),

    path('join_us', view=join_us, name='join_us'),

    path('story/<str:story_id>', view=story, name='story')
]