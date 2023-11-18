import json

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.orders.models import OrderProduct

from .models import Product


class ProductDetailView(TemplateView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "detail.html", {"product": product})


def get_disabled_dates(_, pk):
    product = get_object_or_404(Product, pk=pk)
    orders = OrderProduct.objects.filter(product=product)

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
