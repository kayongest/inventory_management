from django import forms  # Only if you still need forms in views
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    Department,
    SubCategory,
    Event,
    ItemRequest,
    RequestedItem,
    StockTransaction,
)
from .forms import (
    UserRegisterForm,
    ItemRequestForm,
    RequestedItemFormSet,
    EventForm,
    ItemForm,
    CategoryForm,
)  # Updated import
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

# Remove the duplicate import: from .forms import UserRegisterForm  # This is already imported above
from .models import Item, Category
from .mixins import (
    CanViewItemMixin,
    CanAddItemMixin,
    CanChangeItemMixin,
    CanDeleteItemMixin,
    CanViewCategoryMixin,
    CanAddCategoryMixin,
    CanChangeCategoryMixin,
    CanDeleteCategoryMixin,
)
