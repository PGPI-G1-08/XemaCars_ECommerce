
from django.contrib import admin
from django.urls import include, path
from apps.products import views
from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path("add/", views.ProductAddView.as_view(), name="product-add"),
    path("", views.ProductListView.as_view(), name="product-list"),
    path("products/details/<int:pk>", ProductDetailView.as_view(), name="product_detail"), 

]
