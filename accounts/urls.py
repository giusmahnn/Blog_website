from django.urls import path
from .views import (
                    signup_view,
                    login_view,
                    logout_view,
                    password_reset_confirm,
                    forgot_password_email,
                    )



urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('password_reset/', forgot_password_email, name='password_reset'),
    path('reset/new/', password_reset_confirm, name='password_reset_confirm'),
]