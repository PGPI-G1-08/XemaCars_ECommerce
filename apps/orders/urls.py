from apps.orders import views
from django.urls import path

urlpatterns = [
    path("all_orders", views.all_orders, name="all-orders"),
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
