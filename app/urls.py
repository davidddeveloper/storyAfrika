from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    first_home_page,
    sign_in,
    sign_out,
    join_us,
    story,
    like_story,
    stories,
    story_view,
    subscribe,
    search,
    CustomPasswordResetView
)

app_name = 'app'

urlpatterns = [
    path('', view=first_home_page, name='home'),
    path('sign_in', view=sign_in, name='sign_in'),
    path('sign_out', view=sign_out, name='sign_out'),

    path('join_us', view=join_us, name='join_us'),

    path('story/<str:story_id>', view=story, name='story'),
    path('story/<str:story_id>/like', view=like_story, name='like_story'),
    path('stories', view=stories, name='stories'),

    path('story_with_title/<str:story_title>', view=story_view,),

    path('subscribe-to-newsletter', view=subscribe, name='subscribe'),

    path('search', view=search, name='search'),
    # Password reset URLs
    #path('password-reset/', 
    #     auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), 
    #     name='password_reset'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
                template_name='user/password_reset_confirm.html',
                success_url=reverse_lazy('app:password_reset_complete')
            ), 
            name='password_reset_confirm',
            ),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
         name='password_reset_complete'),   
]