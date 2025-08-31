from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout  # Add logout import
from .forms import UserRegisterForm

# Basic homepage with - navbar, buttons for login and signup etc.
class Index(TemplateView):
    template_name = 'inventory/index.html'

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})

class LogoutView(View):
    def post(self, request):  
        logout(request)
        return redirect('index')