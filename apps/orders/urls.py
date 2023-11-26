from apps.orders import views
from django.urls import path
from .views import add_order

urlpatterns = [
    path("all_orders", views.all_orders, name="all-orders"),
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
]