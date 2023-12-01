from apps.complaints.views import ComplaintCreateView, ComplaintListView, ComplaintAnswerView, ComplaintAllView
from django.urls import path

urlpatterns = [
    path(
        "add",
        ComplaintCreateView.as_view(),
        name="add-complaint",
    ),
    path("", ComplaintListView.as_view(), name="complaints"),
    path("list", ComplaintAllView.as_view(), name="complaints-list"),
    path("answer/<int:pk>", ComplaintAnswerView.as_view(), name="answer-complaint")
]
