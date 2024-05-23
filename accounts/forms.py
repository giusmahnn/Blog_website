from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'age',
        )

    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'age',
        )



class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')

    #     if username and password:
    #         user = authenticate(username=username, password=password)
            
    #         if not user:
    #             raise forms.ValidationError("invalid username and password")
    #         elif not username:
    #             raise forms.ValidationError("Wrong username")
    #         elif not password:
    #             raise forms.ValidationError("Wrong Password")
    #         return cleaned_data
        

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Password doesn't match")
        return cleaned_data
    

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")
        return cleaned_data


class OTPValidationForm(SetPasswordForm):
    otp = forms.CharField(max_length=6, required=True, help_text="Enter the OTP sent to your email")