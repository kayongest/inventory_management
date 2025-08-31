from django.urls import path
from .views import Index, SignUpView, LogoutView  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Use your custom LogoutView
]