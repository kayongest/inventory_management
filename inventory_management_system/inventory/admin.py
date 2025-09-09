from django.contrib import admin
from .models import (
    Category,
    Item,
    StockTransaction,
    Department,
    SubCategory,
    Event,
    ItemRequest,
    RequestedItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "sku", "quantity", "status", "location"]
    list_filter = ["category", "status", "department"]
    search_fields = ["name", "sku"]


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ["item", "transaction_type", "quantity", "created_at"]
    list_filter = ["transaction_type", "created_at"]





@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "location"]
    list_filter = ["start_date"]


@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ["event", "requested_by", "status", "created_at"]
    list_filter = ["status", "department"]


@admin.register(RequestedItem)
class RequestedItemAdmin(admin.ModelAdmin):
    list_display = ["item_request", "item", "quantity"]

