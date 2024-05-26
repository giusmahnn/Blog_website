from django.shortcuts import redirect, render, get_object_or_404

from accounts.models import CustomUser
from .forms import (CustomUserCreationForm,
                    CustomLoginForm,
                    CustomUserChangeForm)
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from .utils import send_email
from django.urls import reverse

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



@login_required
def profile_edit(request, username):
    if request.method == 'GET':
        form = CustomUserChangeForm(instance=request.user)
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'username': username}))
    return render(request, 'accounts/profile_edit.html', {'form': form})


def my_profile(request, username):
    # gets the username from the model
    user = get_object_or_404(CustomUser, username=username)
    # checks if the user is logged in and the profile is requested by the logged in user
    # it then grants editing functionalities
    editable = request.user.is_authenticated and request.user.username == username
    return render(request, 'accounts/profile.html', {'profile_user': user, 'editable': editable})

def login_view(request):
    if request.method == 'POST':
        # shows the login form
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid") # for debugging 
            username = form.cleaned_data.get("username") # it shows the field for username
            password = form.cleaned_data.get("password") # it shows the field for password
            print("Username:", username)
            print("Entered Password:", password)
            # it authenticates the user details that they are correct
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authenticated user:", user.username)
                login(request, user)
                return redirect('post_list')
            else:
                print("Authentication failed")
                form.add_error(None, "Invalid username or password")
        else:
            print("Form is not valid")
    else:
        # if the details are wrong it prompts the user to enter details again
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def forgot_password_email(request):
    if request.method == "POST":
        # gets the email via post method
        email = request.POST.get("email")
        user = CustomUser.objects.get(email=email) # it gets the email from the model and ensures its the same
        otp = user.save_otp() # saves the otp to the requested user
        user.save()

        context = {
            "username": user.username,
            "otp": user.otp_field,
        }

        template = render_to_string("accounts/password_reset_email.html", context)

        send_email(email, template, "Password Reset") # uses the ssend mail funtion to send a mail to the requested user
        return render(request, "accounts/password_reset_confirm.html")
    return render(request, "accounts/password_reset.html")


def password_reset_confirm(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/password_reset_confirm.html")

        try:
            user = CustomUser.objects.get(otp_field=otp)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid OTP.")
            # return render(request, "accounts/password_reset_confirm.html")
        user.set_password(new_password)
        user.otp = ''  # Clear OTP after successful password reset
        user.save()
        messages.success(request, "Password has been reset successfully.")
        return redirect("login")
    return render(request, "accounts/password_reset_confirm.html")

