from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        permissions = [
            ("can_view_category", "Can view category"),
            ("can_add_category", "Can add category"),
            ("can_change_category", "Can change category"),
            ("can_delete_category", "Can delete category"),
        ]
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Sub Categories"
        ordering = ['name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    barcode = models.CharField(max_length=100, blank=True, null=True)
    
    # Stock information
    quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=10)
    max_stock_level = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=100, blank=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    stock_controller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='controlled_items')
    
    class Meta:
        ordering = ['name']
        permissions = [
            ("can_view_item", "Can view item"),
            ("can_add_item", "Can add item"),
            ("can_change_item", "Can change item"),
            ("can_delete_item", "Can delete item"),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level

class ItemRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    ]

    project_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_requests')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='item_requests')
    items = models.ManyToManyField(Item, through='RequestedItem')
    stock_location = models.CharField(max_length=200)
    requested_by = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_at = models.DateTimeField(null=True, blank=True)
    required_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Request #{self.id} - {self.event.name}"

class RequestedItem(models.Model):
    item_request = models.ForeignKey(ItemRequest, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = ['item_request', 'item']

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"