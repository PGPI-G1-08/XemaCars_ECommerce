from django.urls import path
from apps.products import views
from .views import ProductDetailView


urlpatterns = [
    path(
        "products/details/<int:pk>", ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "products/disabled_dates/<int:pk>",
        views.get_disabled_dates,
        name="product_disabled_dates",
    ),
]
