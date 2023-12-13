from django.shortcuts import render, redirect

from apps.products.forms import FilterForm
from apps.products.models import Product


# Create your views here.
def index(request):
    form = FilterForm(request.POST)
    products = Product.objects.all()
    top_products = sorted(products, key=lambda x: x.average_rating, reverse=True)[:3]
    print(top_products)
    if form.is_valid():
        if form.cleaned_data["nombre"]:
            name = form.cleaned_data["nombre"]
            for product in products:
                product.complete_name = product.name + " " + product.brand

            products = [
                product
                for product in products
                if name.lower() in product.complete_name.lower()
            ]

        products = [product.id for product in products]
        request.session["products"] = products
        request.session["form"] = form.cleaned_data
        return redirect("/products")
    else:
        return render(
            request, "home.html", {"form": form, "top_products": top_products}
        )


def about_us(request):
    return render(request, "about_us.html")


def design_kit(request):
    return render(request, "design_kit.html")
