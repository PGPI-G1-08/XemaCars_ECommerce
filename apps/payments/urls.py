from apps.payments import views
from django.urls import path


urlpatterns = [
    path(
        "delete/<str:payment_method_id>",
        views.delete,
        name="payment_method_delete",
    ),
]
