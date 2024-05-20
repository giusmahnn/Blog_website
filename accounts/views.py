from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy

#from django.views. generic import TemplateView
# Create your views here.


def home_view(request):
    return render(request, 'home.html')

class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})




def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')



    


