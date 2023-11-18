from apps.cart import views
from django.urls import path

urlpatterns = [
    path("", views.get_cart, name="cart"),
    path("add", views.add_to_cart, name="add_to_cart"),
    path("count", views.get_cart_count, name="get_cart_count"),
]
