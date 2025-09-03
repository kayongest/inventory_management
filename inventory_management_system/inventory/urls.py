from django.urls import path
from .views import (
    Index,
    SignUpView,
    DashboardView,
    ItemListView,
    CategoryListView,
    ItemCreateView,
    ItemDetailView,
    ItemUpdateView,
    ItemDeleteView,
    print_item_detail,
    CategoryCreateView, 
    CategoryDeleteView, 
    CategoryUpdateView,
    
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="inventory/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="inventory/logout.html"),
        name="logout",
    ),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Inventory URLs
    path("items/", ItemListView.as_view(), name="item-list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("item/new/", ItemCreateView.as_view(), name="item-create"),
    path("item/<int:pk>/edit/", ItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
    path("item/<int:pk>/print/", print_item_detail, name="print-item"),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/new/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('item/<int:pk>/print/', print_item_detail, name='item-print'),
]
