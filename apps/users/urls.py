from django.urls import path
from .views import LoginView, logout_view, RegisterView, UserListView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("signin/", LoginView.as_view(), name="signin"),
    path("logout/", logout_view, name="logout"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("users/list/", UserListView.as_view(), name="users_list"),
]
