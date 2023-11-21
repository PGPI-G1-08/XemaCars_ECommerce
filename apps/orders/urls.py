from apps.orders import views
from django.urls import path
from .views import add_order

urlpatterns = [
    path("add", views.add_order, name="add_order"),
]
