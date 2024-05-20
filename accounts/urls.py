from django.urls import path
from .views import home_view, CustomSignUpView, login_view, logout_view
#from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
    
]