from django.contrib import admin
from .models import Category, Item, InventoryTransaction, Supplier, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'quantity', 'selling_price', 'status']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['name', 'sku', 'barcode']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'sku', 'barcode')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory', {
            'fields': ('quantity', 'min_stock_level', 'max_stock_level', 'status', 'location', 'shelf')
        }),
        ('Additional Info', {
            'fields': ('supplier', 'created_by', 'last_restocked')
        }),
    )

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'created_at', 'created_by']
    list_filter = ['transaction_type', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone']
    search_fields = ['name', 'contact_person']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'is_inventory_manager']