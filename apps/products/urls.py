from django.contrib import admin
from django.urls import include, path
from apps.products import views
from django.urls import path
from apps.products import views
from .views import ProductDetailView, CarSearchView


urlpatterns = [
    path(
        "products/details/<int:pk>", ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "products/disabled_dates/<int:pk>",
        views.get_disabled_dates,
        name="product_disabled_dates",
    ),
    path("add/", views.ProductAddView.as_view(), name="product-add"),
    path("car_search/", CarSearchView.as_view(), name="car_search"),
    path("", views.ProductListView.as_view(), name="product-list"),
]
