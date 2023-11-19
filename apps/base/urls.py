from apps.base import views
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("", views.index, name="homepage"),
    path("about-us", views.about_us, name="about-us"),
    path("design-kit/", views.design_kit, name="design-kit"),
    path("cart/", include("apps.cart.urls")),
]
