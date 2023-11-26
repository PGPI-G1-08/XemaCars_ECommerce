from django.contrib import admin
from django.urls import include, path
from apps.products import views
from django.urls import path
from .views import ProductDetailView, ProductUpdateView, ProductDeleteView, CarSearchView


urlpatterns = [
    path("add/", views.ProductAddView.as_view(), name="product-add"),
    path("car_search/", CarSearchView.as_view(), name="car_search"),
    path("", views.ProductListView.as_view(), name="product-list"),
    path("products/details/<int:pk>", ProductDetailView.as_view(), name="product_detail"), 
    path("products/details/<int:pk>/delete", ProductDeleteView.as_view(), name="delete"),
    path("products/details/<int:pk>/edit", ProductUpdateView.as_view(), name="edit"), 
]