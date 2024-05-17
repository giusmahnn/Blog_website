from django.urls import path
from .views import CustomSignUpView, CustomLoginView, HomePageView, CustomLogoutView



urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]