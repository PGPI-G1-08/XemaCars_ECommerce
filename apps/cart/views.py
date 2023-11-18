import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from apps.products.models import Product


@login_required(login_url="/signin")
def get_cart(request):
    customer = request.user.customer
    cart_products = customer.cart.products.all()

    return render(
        request,
        "cart.html",
        {"cart_products": cart_products, "total": customer.cart.total},
    )


@login_required(login_url="/signin")
def add_to_cart(request):
    if request.method != "POST":
        return

    product_id = request.POST.get("product_id")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    product = Product.objects.get(pk=product_id)
    request.user.cart.products.add(product, start_date, end_date)

    return render(
        request,
        "cart.html",
        {
            "cart_products": request.user.cart.products.all(),
            "total": request.user.cart.total,
        },
    )


@login_required(login_url="/signin")
def get_cart_count(request):
    response_data = {}
    response_data["count"] = request.user.cart.products.count()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
