from django.shortcuts import render

from apps.products.forms import FilterForm
from apps.products.models import Product


# Create your views here.
def index(request):
    form = FilterForm(request.POST)
    if form.is_valid():
        products = Product.objects.all()
        if form.cleaned_data["nombre"]:
            name = form.cleaned_data["nombre"]
            for product in products:
                product.complete_name = product.name + " " + product.brand

            products = [
                product
                for product in products
                if name.lower() in product.complete_name.lower()
            ]
        return render(
            request, "product-list.html", {"products": products, "form": form}
        )
    else:
        return render(request, "home.html", {"form": form})


def about_us(request):
    return render(request, "about_us.html")


def design_kit(request):
    return render(request, "design_kit.html")
