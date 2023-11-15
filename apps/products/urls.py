from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path("products/details/<int:pk>", ProductDetailView.as_view(), name="product_detail"),   
    
]
