from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from apps.products.models import Product
from .models import CartProduct


@login_required(login_url="/signin")
def get_cart(request):
    customer = request.user.customer
    # Get CartProducts
    cart_products = CartProduct.objects.filter(cart=customer.cart)

    return render(
        request,
        "cart.html",
        {"cart_products": cart_products, "total": customer.cart.total},
    )


@login_required(login_url="/signin")
def add_to_cart(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        product_id = data["product_id"]
        from_date = data["from_date"]
        to_date = data["to_date"]

        start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        product = Product.objects.get(pk=product_id)
        request.user.customer.cart.add(product, start_date, end_date)

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(json.dumps({}), status=200, content_type="application/json")


@login_required(login_url="/signin")
def remove_from_cart(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        product_id = data["product_id"]

        product = Product.objects.get(pk=product_id)
        request.user.customer.cart.products.remove(product)

        new_price = request.user.customer.cart.total

    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(
        json.dumps({"new_price": new_price}),
        status=200,
        content_type="application/json",
    )


@login_required(login_url="/signin")
def get_cart_count(request):
    response_data = {}
    response_data["count"] = request.user.customer.cart.products.count()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def has_product(request, product_id):
    if request.user == None or request.user.is_anonymous:
        return HttpResponse(
            json.dumps({"has_product": False}), content_type="application/json"
        )

    response_data = {}
    response_data["has_product"] = request.user.customer.cart.products.filter(
        pk=product_id
    ).exists()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
