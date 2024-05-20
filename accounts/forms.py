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

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email or not email.strip():
            raise forms.ValidationError("Input a correct email address")
        
        if CustomUser.objects.filter(email__iexact=email).exists:
            raise forms.ValidationError("Email address already exists")
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username__iexact=username).exists:
            raise forms.ValidationError("Username already exists")
        return username
    
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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise forms.ValidationError("invalid username and password")
            elif not username:
                raise forms.ValidationError("Wrong username")
            elif not password:
                raise forms.ValidationError("Wrong Password")
            return cleaned_data