from apps.complaints.views import ComplaintCreateView, ComplaintListView
from django.urls import path

urlpatterns = [
    path(
        "add",
        ComplaintCreateView.as_view(),
        name="add-complaint",
    ),
    path("", ComplaintListView.as_view(), name="complaints"),
]
