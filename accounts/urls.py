from django.urls import path
from .views import home_view, CustomSignUpView, login_view, logout_view



urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
    
]