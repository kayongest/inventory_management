from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin  
from .forms import UserRegisterForm
from .models import Item, Category
from django.views.generic import ListView

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

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dashboard statistics
        context['total_items'] = Item.objects.count()
        context['total_categories'] = Category.objects.count()
        
        # More statistics 
        context['low_stock_items'] = 1  # Default
        context['out_of_stock_items'] = 23  # Default
        
        return context
    
class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

class CategoryListView(ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'inventory/item_form.html'
    fields = ['name', 'description', 'category', 'sku', 'barcode', 
              'cost_price', 'selling_price', 'quantity', 'min_stock_level',
              'max_stock_level', 'status', 'location', 'shelf', 'supplier']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)