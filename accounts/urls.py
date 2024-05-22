from django.urls import path
from .views import (home_view,
                    signup_view,
                    login_view,
                    logout_view,
                    profile_view,
                    my_profile,
                    password_reset_request,
                    password_reset_done,
                    password_reset_confirm,
                    password_reset_complete)



urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', my_profile, name='profile'),
    path('profile/edit/', profile_view, name='edit_profile'),
    path('login/', login_view, name='login'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_done/', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
    
]