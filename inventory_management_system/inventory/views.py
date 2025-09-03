from django.db import models
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
from .forms import UserRegisterForm
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


# Basic homepage with - navbar, buttons for login and signup etc.
class Index(TemplateView):
    template_name = "inventory/index.html"


class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "inventory/signup.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("index")
        return render(request, "inventory/signup.html", {"form": form})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # This shows item counts only if the logged in user has permission to view items
        if self.request.user.has_perm("inventory.can_view_item"):
            context["total_items"] = Item.objects.count()
            context["low_stock_items"] = Item.objects.filter(
                quantity__lte=models.F("min_stock_level")
            ).count()
            context["out_of_stock_items"] = Item.objects.filter(quantity=0).count()
        else:
            context["total_items"] = "N/A"
            context["low_stock_items"] = "N/A"
            context["out_of_stock_items"] = "N/A"

        # Only show category count if user has permission to view categories
        if self.request.user.has_perm("inventory.can_view_category"):
            context["total_categories"] = Category.objects.count()
        else:
            context["total_categories"] = "N/A"

        # Add permission flags to context for template logic
        context["can_view_items"] = self.request.user.has_perm(
            "inventory.can_view_item"
        )
        context["can_view_categories"] = self.request.user.has_perm(
            "inventory.can_view_category"
        )
        context["can_add_items"] = self.request.user.has_perm("inventory.can_add_item")
        context["can_add_categories"] = self.request.user.has_perm(
            "inventory.can_add_category"
        )

        return context

# Item views
class ItemListView(LoginRequiredMixin, CanViewItemMixin, ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        # This will only be called if the user has permission based on the mixin
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        location = self.request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(sku__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = dict(Item.STATUS_CHOICES)
        context["locations"] = (
            Item.objects.exclude(location="")
            .values_list("location", flat=True)
            .distinct()
        )
        # Add permission flags for template
        context["can_add_items"] = self.request.user.has_perm("inventory.can_add_item")
        context["can_change_items"] = self.request.user.has_perm(
            "inventory.can_change_item"
        )
        context["can_delete_items"] = self.request.user.has_perm(
            "inventory.can_delete_item"
        )
        return context


class ItemDetailView(LoginRequiredMixin, CanViewItemMixin, DetailView):
    model = Item
    template_name = "inventory/item_detail.html"


class ItemCreateView(LoginRequiredMixin, CanAddItemMixin, CreateView):
    model = Item
    template_name = "inventory/item_form.html"
    fields = [
        "name",
        "description",
        "category",
        "sku",
        "barcode",
        "cost_price",
        "selling_price",
        "quantity",
        "min_stock_level",
        "max_stock_level",
        "status",
        "location",
        "shelf",
        "supplier",
    ]
    success_url = reverse_lazy("item-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, CanChangeItemMixin, UpdateView):
    model = Item
    template_name = "inventory/item_form.html"
    fields = [
        "name",
        "description",
        "category",
        "sku",
        "barcode",
        "cost_price",
        "selling_price",
        "quantity",
        "min_stock_level",
        "max_stock_level",
        "status",
        "location",
        "shelf",
        "supplier",
    ]
    success_url = reverse_lazy("item-list")


class ItemDeleteView(LoginRequiredMixin, CanDeleteItemMixin, DeleteView):
    model = Item
    template_name = "inventory/item_confirm_delete.html"
    success_url = reverse_lazy("item-list")


# Category views
class CategoryListView(LoginRequiredMixin, CanViewCategoryMixin, ListView):
    model = Category
    template_name = "inventory/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, CanAddCategoryMixin, CreateView):
    model = Category
    template_name = "inventory/category_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("category-list")


class CategoryUpdateView(LoginRequiredMixin, CanChangeCategoryMixin, UpdateView):
    model = Category
    template_name = "inventory/category_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("category-list")


class CategoryDeleteView(LoginRequiredMixin, CanDeleteCategoryMixin, DeleteView):
    model = Category
    template_name = "inventory/category_confirm_delete.html"
    success_url = reverse_lazy("category-list")


def print_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "inventory/print_item.html", {"item": item})


def permission_denied_view(request, exception=None):
    """Custom 403 error page"""
    return render(request, "403.html", status=403)


def csrf_failure(request, reason=""):
    """Custom CSRF failure page"""
    context = {"reason": reason}
    return render(request, "403_csrf.html", context)
