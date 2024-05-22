from django.shortcuts import redirect, render

from accounts.models import CustomUser
from .forms import (CustomUserCreationForm,
                    CustomLoginForm,
                    CustomUserChangeForm,
                    PasswordResetRequestForm,
                    SetPasswordForm,
                    OTPValidationForm)
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.template.loader import render_to_string
from .utils import otp_generation, send_email
from django.views import View

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
def profile_view(request):
    if request.method == 'GET':
        form = CustomUserChangeForm(instance=request.user)
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def my_profile(request):
    return render(request, 'profile.html', {'user': request.user})

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
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def forgot_password_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.get(email=email)
        otp = user.save_otp()
        user.save()

        context = {
            "username": user.username,
            "otp": user.otp_field,
        }

        template = render_to_string("accounts/password_reset_email.html", context)

        send_email(email, template, "Password Reset")
        return render(request, "accounts/password_reset_confirm.html")
    return render(request, "accounts/password_reset.html")


def password_reset_confirm(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = CustomUser.objects.get(otp_field=otp)

        user.set_password(new_password)
        return redirect("login")
    return render(request, "accounts/password_reset_confirm.html")

# User = get_user_model()    
# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetRequestForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data['email']
#             associated_users = User.objects.filter(email=data)
#             if associated_users.exists():
#                 for user in associated_users:
#                     # Generate and save OTP
#                     user.save_otp()

#                     # Send the email
#                     try:
#                         send_email(user, request.META['HTTP_HOST'])
#                         messages.success(request, 'A password reset OTP has been sent to your email.')
#                         return redirect('password_reset_done')
#                     except Exception as e:
#                         messages.error(request, f'Error sending email: {e}')
#                         return render(request, "registration/password_reset.html", {"form": form})
#             else:
#                 messages.error(request, 'No user is associated with this email address.')
#                 return render(request, "registration/password_reset.html", {"form": form})
#             return redirect('password_reset_otp')
#     else:
#         form = PasswordResetRequestForm()
#     return render(request, "registration/password_reset.html", {"form": form})


# def password_reset_confirm(request, uidb64=None):
#     if request.method == "POST":
#         form = OTPValidationForm(request.POST)
#         if form.is_valid():
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             try:
#                 user = User.objects.get(pk=uid)
#             except User.DoesNotExist:
#                 messages.error(request, "Invalid user.")
#                 return render(request, "registration/password_reset_confirm.html", {"form": form})
            
#             if user.otp_is_valid() and form.cleaned_data['otp'] == user.otp:
#                 user.set_password(form.cleaned_data['new_password1'])
#                 user.otp = None  # Clear the OTP after successful password reset
#                 user.otp_created_at = None
#                 user.save()
#                 messages.success(request, "Your password has been set. You can now log in.")
#                 return redirect("/password_reset_complete/")
#             else:
#                 messages.error(request, "Invalid OTP or OTP has expired.")
#                 return render(request, "registration/password_reset_confirm.html", {"form": form})
#         else:
#             messages.error(request, "Please correct the error below.")
#     else:
#         form = OTPValidationForm()
#     return render(request, "registration/password_reset_confirm.html", {"form": form})

# def password_reset_done(request):
#     return render(request, "registration/password_reset_done.html")

# def password_reset_complete(request):
#     return render(request, "registration/password_reset_complete.html")