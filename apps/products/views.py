import json

from apps.orders.models import OrderProduct
from apps.opinions.models import Opinion
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import ProductForm, FilterForm, OpinionForm
from .models import Product


class ProductAddView(TemplateView):
    def post(self, request):
        if request.method == "POST":
            post = request.POST.copy()
            post["price"] = post["price"].replace(",", ".")
            request.POST = post
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
        if request.session.get("products") is not None:
            products_session = request.session["products"]
            products = Product.objects.filter(id__in=products_session)
            form = FilterForm(request.session["form"])
            del request.session["products"]
            del request.session["form"]
        else:
            products = Product.objects.all()
        return render(
            request, "product-list.html", {"products": products, "form": form}
        )

    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():
            products = Product.objects.all()
            available = form.cleaned_data["solo_disponibles"]
            if available is True:
                products = products.filter(available=available)
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
            if form.cleaned_data["nombre"]:
                name = form.cleaned_data["nombre"]
                for product in products:
                    product.complete_name = product.name + " " + product.brand

                products = [
                    product
                    for product in products
                    if name.lower() in product.complete_name.lower()
                ]
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

# ADMIN
class ProductDeleteView(TemplateView):
    def get(self, request, pk):
        if request.user.is_superuser:
            product = get_object_or_404(Product, pk=pk)
            return render(request, "delete.html", {"product": product})
        else:
            return render(request, "forbidden.html")

    def post(self, request, pk):
        if request.user.is_superuser:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return redirect("http://127.0.0.1:8000/products")
        else:
            return render(request, "forbidden.html")


class ProductUpdateView(TemplateView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        if request.user.is_superuser:
            return render(request, "edit.html", {"product": product, "form": form})
        else:
            return render(request, "forbidden.html")

    def post(self, request, pk):
        if request.user.is_superuser:
            product = get_object_or_404(Product, pk=pk)
            post = request.POST.copy()
            post["price"] = post["price"].replace(",", ".")
            request.POST = post
            form = ProductForm(request.POST)
            if request.method == "POST":
                if form.is_valid():
                    if form.cleaned_data.get("name"):
                        product.name = form.cleaned_data.get("name")
                    if form.cleaned_data.get("brand"):
                        product.brand = form.cleaned_data.get("brand")
                    if form.cleaned_data.get("year"):
                        product.year = form.cleaned_data.get("year")
                    if form.cleaned_data.get("combustion_type"):
                        product.combustion_type = form.cleaned_data.get(
                            "combustion_type"
                        )
                    if form.cleaned_data.get("description"):
                        product.description = form.cleaned_data.get("description")
                    if form.cleaned_data.get("price"):
                        product.price = form.cleaned_data.get("price")
                    if form.cleaned_data.get("image_url"):
                        product.image_url = form.cleaned_data.get("image_url")
                    product.available = form.cleaned_data.get("available")
                    product.save()
                    return redirect("/products")
                else:
                    return render(
                        request, "edit.html", {"product": product, "form": form}
                    )
        else:
            return render(request, "forbidden.html")
