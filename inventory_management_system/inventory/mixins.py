from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


# Base mixin for all permission checks
class PermissionRedirectMixin:
    permission_denied_message = "You don't have permission to access this resource."
    redirect_url = "dashboard"  # This serves as a default redirect

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, self.permission_denied_message)
            return redirect(self.redirect_url)
        else:
            messages.info(self.request, "Please login to access this page.")
            return redirect("login")


# Items' permissions
class CanViewItemMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_view_item")

    permission_denied_message = "You don't have permission to view items."
    redirect_url = "dashboard"


class CanAddItemMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_add_item")

    permission_denied_message = "You don't have permission to add items."
    redirect_url = "item-list"


class CanChangeItemMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_change_item")

    permission_denied_message = "You don't have permission to change items."
    redirect_url = "item-list"


class CanDeleteItemMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_delete_item")

    permission_denied_message = "You don't have permission to delete items."
    redirect_url = "item-list"


# Category permissions
class CanViewCategoryMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_view_category")

    permission_denied_message = "You don't have permission to view categories."
    redirect_url = "dashboard"


class CanAddCategoryMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_add_category")

    permission_denied_message = "You don't have permission to add categories."
    redirect_url = "category-list"


class CanChangeCategoryMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_change_category")

    permission_denied_message = "You don't have permission to change categories."
    redirect_url = "category-list"


class CanDeleteCategoryMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_delete_category")

    permission_denied_message = "You don't have permission to delete categories."
    redirect_url = "category-list"

class CanViewItemMixin(PermissionRedirectMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm("inventory.can_view_item")

    permission_denied_message = "You don't have permission to view items."
    redirect_url = "dashboard"