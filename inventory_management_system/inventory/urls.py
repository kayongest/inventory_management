from django.urls import path
from .views import Index, SignUpView, DashboardView, ItemListView, CategoryListView, ItemCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # adding new URLs
    path('items/', ItemListView.as_view(), name='item-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'), 
]