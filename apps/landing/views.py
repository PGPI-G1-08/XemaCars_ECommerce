from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "home.html")


def about_us(request):
    return render(request, "about_us.html")


def design_kit(request):
    return render(request, "design_kit.html")
