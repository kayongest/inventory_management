from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
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
    # Items
    path("items/", ItemListView.as_view(), name="item-list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("item/new/", ItemCreateView.as_view(), name="item-create"),
    path("item/<int:pk>/edit/", ItemUpdateView.as_view(), name="item-update"),
    path("item/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
    path("item/<int:pk>/print/", print_item_detail, name="print-item"),
    # Categories
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("category/new/", CategoryCreateView.as_view(), name="category-create"),
    path(
        "category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-update"
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    # Events
    path("events/", EventListView.as_view(), name="event-list"),
    path("event/new/", EventCreateView.as_view(), name="event-create"),
    path("event/<int:pk>/edit/", EventUpdateView.as_view(), name="event-update"),
    path("event/<int:pk>/delete/", EventDeleteView.as_view(), name="event-delete"),
    # Requests
    path("requests/", ItemRequestListView.as_view(), name="request-list"),
    path("request/new/", create_item_request, name="request-create"),
    path("request/<int:pk>/approve/", approve_item_request, name="request-approve"),
    # Reports
    path("reports/", reports_view, name="reports"),
    path("reports/print/<str:report_type>/", print_report, name="print-report"),
]
