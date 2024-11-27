from django.urls import path
from .views import first_home_page

urlpatterns = [
    path('', view=first_home_page, name='home'),
]