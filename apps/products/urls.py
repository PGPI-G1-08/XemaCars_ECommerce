from django.contrib import admin
from django.urls import include, path
from apps.products import views

urlpatterns = [
    path("add/", views.ProductAddView.as_view(), name="product-add"),
    path("", views.ProductListView.as_view(), name="product-list"),
]
