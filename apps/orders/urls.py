from apps.orders import views
from django.urls import path
from .views import add_order

urlpatterns = [
    path(
        "my_order_detail/<str:order_identifier>/",
        views.my_order_detail,
        name="my_order_detail",
    ),
    path("search_order", views.search_order, name="search_order"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("all_orders", views.AdminOrdersView.as_view(), name="all-orders"),
    path("add", views.add_order, name="add_order"),
    path(
        "cancel_orderproduct/<int:orderproduct_id>/",
        views.cancel_orderproduct,
        name="cancel_orderproduct",
    ),
    path(
        "cancel_order/<int:order_id>/",
        views.cancel_order,
        name="cancel_order",
    ),
    path("client_orders", views.client_orders, name="client-orders"),
]
