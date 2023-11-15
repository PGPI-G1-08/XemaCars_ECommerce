from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import Product

class ProductDetailView(TemplateView):
    def get(self, request, pk):
        product =get_object_or_404(Product, pk=pk)
        return render(request, "detail.html", {"product": product})
