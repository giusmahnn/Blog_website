from django.urls import path
from .views import CustomSignUpView, CustomLoginView, login_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login')
    
]