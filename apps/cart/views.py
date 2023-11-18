from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

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

    try:
        data = json.loads(request.body)

        product_id = data["product_id"]
        from_date = data["from_date"]
        to_date = data["to_date"]

        start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        product = Product.objects.get(pk=product_id)
        request.user.customer.cart.add(product, start_date, end_date)

    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}), status=400)

    return HttpResponse(json.dumps({}), status=200, content_type="application/json")


@login_required(login_url="/signin")
def get_cart_count(request):
    response_data = {}
    response_data["count"] = request.user.customer.cart.products.count()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
