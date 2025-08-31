from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterFrom(UserCreationForm):
    # created an email filed coz it doesn't come by default
    email = forms.EmailField()    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']