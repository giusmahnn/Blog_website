from django.urls import path
from .views import CustomSignUpView, CustomLoginView, HomePageView



urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]