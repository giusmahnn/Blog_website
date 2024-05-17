from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views. generic import TemplateView
# Create your views here.



class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'

class HomePageView(TemplateView):
    template_name = 'home.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')