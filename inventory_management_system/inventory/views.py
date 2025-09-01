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

        # Dashboard statistics
        context["total_items"] = Item.objects.count()
        context["total_categories"] = Category.objects.count()

        # More statistics
        context["low_stock_items"] = 1  # Default
        context["out_of_stock_items"] = 23  # Default

        return context


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by status if provided
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Filter by location if provided
        location = self.request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Search by name or description if provided
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

        # Get unique locations for filter dropdown
        context["locations"] = (
            Item.objects.exclude(location="")
            .values_list("location", flat=True)
            .distinct()
        )

        return context


def print_item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "inventory/print_item.html", {"item": item})


# Add these views for item operations
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "inventory/item_detail.html"


class ItemUpdateView(LoginRequiredMixin, UpdateView):
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


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "inventory/item_confirm_delete.html"
    success_url = reverse_lazy("item-list")


class ItemCreateView(LoginRequiredMixin, CreateView):
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


class CategoryListView(ListView):
    model = Category
    template_name = "inventory/category_list.html"
    context_object_name = "categories"
