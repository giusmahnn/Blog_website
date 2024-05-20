from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.


def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    '''
    creates a signup form for the user, then saves all fields that are imputed by the user
    if the fields are valid it saves it and redirects the user to login.
    if they are not valid it prompts the user to try again
    '''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    '''
    creates an instance for the user to impute the login details, it then extracts the username and 
    password from the cleaned data and checks it for authentication. 
    if the user is valid it logs the user in and redirects the user to the post list page if not,
    it prompts the user to enter details again.
    '''
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



    


