from apps.cart import views
from django.urls import path

urlpatterns = [
    path("", views.get_cart, name="cart"),
    path("add", views.add_to_cart, name="add_to_cart"),
    path("remove", views.remove_from_cart, name="remove_from_cart"),
    path("count", views.get_cart_count, name="get_cart_count"),
    path("has_product/<int:product_id>", views.has_product, name="has_product"),
]
