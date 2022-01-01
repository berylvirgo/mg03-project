from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.forms import fields

from .models import *
from users.models import User


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False) # and add the remember_me field

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Enter Email Address...'})

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Enter Password'})

        self.fields['remember_me'].widget.attrs.update(
            {'class': 'custom-control-input', 'id': 'customCheck'})


class SignUpForm(UserCreationForm):

    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'name',
            'email', 
            'password1', 
            'password2', 
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Full Name', 'required': True})

        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Email Address'})

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Password'})

        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Repeat Password'})


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-user', 'placeholder': 'Enter Email Address...'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'bio',
            'phone_number',
            'date_of_birth',
            'profile_image'
        ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['is_read']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Your Name *', })
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Your Email *', })

        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Your Phone Number *', })
        self.fields['body'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Your Message *', })
