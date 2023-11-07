# import render
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ProductForm


class ProductAddView(TemplateView):
    def post(self, request):
        form = ProductForm(request.POST)
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
