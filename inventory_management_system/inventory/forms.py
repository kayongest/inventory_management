from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item, Category, ItemRequest, RequestedItem, Event, Department


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = [
            "event",
            "department",
            "required_date",
            "notes",
            "stock_location",
            "requested_by",
        ]
        widgets = {
            "required_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class RequestedItemForm(forms.ModelForm):
    class Meta:
        model = RequestedItem
        fields = ["item", "quantity"]


# Create a formset for requested items
RequestedItemFormSet = forms.inlineformset_factory(
    ItemRequest, RequestedItem, form=RequestedItemForm, extra=1, can_delete=True
)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "start_date", "end_date", "location", "description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "description",
            "category",
            "subcategory",
            "sku",
            # REMOVED: "barcode" - field doesn't exist in model
            # REMOVED: "cost_price" - field doesn't exist in model
            # REMOVED: "selling_price" - field doesn't exist in model
            # REMOVED: "shelf" - field doesn't exist in model
            # REMOVED: "supplier" - field doesn't exist in model
            "quantity",
            "min_stock_level",
            "max_stock_level",
            "status",
            "location",
            "department",
            "stock_controller",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }