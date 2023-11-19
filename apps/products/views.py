from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ProductForm
from .models import Product
from django.shortcuts import get_object_or_404


class ProductAddView(TemplateView):
    def post(self,request):
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
                return redirect('/')  

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
        products = Product.objects.all()
        return render(request, "product-list.html", {"products": products})

class ProductDetailView(TemplateView):
    def get(self, request, pk):
        product =get_object_or_404(Product, pk=pk)
        return render(request, "detail.html", {"product": product})
