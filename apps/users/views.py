from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework.views import APIView
import logging

from .forms import LoginForm
from .models import Customer

from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from apps.users.forms import LoginForm, RegisterForm


class LoginView(TemplateView):
    def post(self, request):
        form = LoginForm(request.POST)
        message = None

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                return redirect("/")
            else:
                message = "Usuario o contraseña incorrectos"
        else:
            message = "Formulario inválido"

        return render(request, "users/login.html", {"form": form, "message": message})

    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


class RegisterView(APIView):
    def post(self, request):
        form = RegisterForm(request.POST)

        message = None

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password1")

            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
            ):
                message = "El usuario ya existe."
            else:
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)
                user.save()

                customer = Customer(user=user, phone_number=phone_number)
                customer.save()

                return redirect("/signin")
        else:
            logging.warning(form.errors.as_text())

        return render(request, "users/signup.html", {"form": form, "message": message})

    def get(self, request):
        form = RegisterForm(None)

        return render(request, "users/signup.html", {"form": form, "message": None})
