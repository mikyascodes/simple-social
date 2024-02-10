from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import  UserCreationForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email','style': 'width:50%'}),
            'username': forms.TextInput(attrs={'placeholder': 'Type your username','style': 'width:50%'}),
            }
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password created', 'style': 'width:50%'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation','style': 'width:50%'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio','profile_status']

        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Avatar',}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio','row':5}),
            'profile_status': forms.CheckboxInput(attrs={'class': 'form-check-input','required':'True'}),
        }

        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username',}),
        }