import json

from apps.orders.models import OrderProduct
from apps.opinions.models import Opinion
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import ProductForm, FilterForm, CarSearchForm, OpinionForm
from .models import Product


class ProductAddView(TemplateView):
    def post(self, request):
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                product = Product(
                    name=form.cleaned_data["name"],
                    brand=form.cleaned_data["brand"],
                    year=form.cleaned_data["year"],
                    combustion_type=form.cleaned_data["combustion_type"],
                    description=form.cleaned_data["description"],
                    price=form.cleaned_data["price"],
                    image_url=form.cleaned_data["image_url"],
                    available=form.cleaned_data["available"],
                )
                product.save()
                return redirect("/")

        else:
            form = ProductForm()

        if request.user.is_superuser:
            return render(request, "product-add.html", {"form": form})
        else:
            return render(request, "forbidden.html")

    def get(self, request):
        form = ProductForm()
        if request.user.is_superuser:
            return render(request, "product-add.html", {"form": form})
        else:
            return render(request, "forbidden.html")


class ProductListView(TemplateView):
    def get(self, request):
        form = FilterForm()
        products = Product.objects.all()
        return render(
            request, "product-list.html", {"products": products, "form": form}
        )

    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():
            available = form.cleaned_data["solo_disponibles"]
            if available is True:
                products = Product.objects.filter(available=available)
            else:
                products = Product.objects.all()
            if form.cleaned_data["año_mínimo"]:
                year = form.cleaned_data["año_mínimo"]
                products = products.filter(year__gte=year)
            if form.cleaned_data["marca"]:
                brand = form.cleaned_data["marca"]
                products = products.filter(brand__icontains=brand)
            if form.cleaned_data["tipo_de_combustión"]:
                combustion_type = form.cleaned_data["tipo_de_combustión"]
                if combustion_type != "No_Filtrar":
                    products = products.filter(combustion_type=combustion_type)
            if form.cleaned_data["precio_máximo"]:
                price = form.cleaned_data["precio_máximo"]
                products = products.filter(price__lte=price)
        else:
            products = Product.objects.all()

        return render(
            request, "product-list.html", {"products": products, "form": form}
        )


class ProductDetailView(TemplateView):
    def get(self, request, pk):
        opinions = Product.objects.get(pk=pk).opinion_set.all()
        product = get_object_or_404(Product, pk=pk)
        form = OpinionForm(initial={"customer": request.user.id, "product": product.id})
        return render(
            request,
            "detail.html",
            {"product": product, "opinions": opinions, "form": form},
        )

    def post(self, request, pk):
        if request.user.is_anonymous:
            return redirect("/signin")

        form = OpinionForm(request.POST)
        opinions = Product.objects.get(pk=pk).opinion_set.all()
        product = get_object_or_404(Product, pk=pk)

        if form.is_valid():
            opinion = Opinion(
                product=Product.objects.get(pk=pk),
                customer=request.user.customer,
                rating=form.cleaned_data["rating"],
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
            )
            opinion.save()

        return render(
            request,
            "detail.html",
            {"product": product, "opinions": opinions, "form": form},
        )


def get_disabled_dates(_, pk):
    product = get_object_or_404(Product, pk=pk)
    orders = OrderProduct.objects.filter(product=product).exclude(cancelled=True)

    data = {}
    disabled_dates = []
    for order in orders:
        disabled_dates.append(
            {
                "start": order.start_date.strftime("%Y-%m-%d"),
                "end": order.end_date.strftime("%Y-%m-%d"),
            }
        )

    data["disabled_dates"] = disabled_dates
    return HttpResponse(json.dumps(data), content_type="application/json")


class CarSearchView(TemplateView):
    def get(self, request):
        formCarSearch = CarSearchForm(request.GET)
        filtered_products = []
        if formCarSearch.is_valid() and formCarSearch.cleaned_data["search"] != "":
            search_query = formCarSearch.cleaned_data["search"]
            products = Product.objects.all()
            for product in products:
                product.complete_name = product.name + " " + product.brand

            filtered_products = [
                product
                for product in products
                if search_query.lower() in product.complete_name.lower()
            ]
        else:
            return redirect("/products")

        products = Product.objects.all()
        return render(request, "product-list.html", {"products": filtered_products})
