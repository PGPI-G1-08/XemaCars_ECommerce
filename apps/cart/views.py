from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from apps.users.forms import EditDeliveryPointAndPaymentMethodForm
from apps.cart.anon_cart import AnonCart
from apps.products.models import Product
from apps.users.models import Customer

from .models import CartProduct

from apps.products.models import DeliveryPoint
from apps.payments.models import PaymentMethod


def get_cart(request):
    if request.user == None or request.user.is_anonymous:
        cart = AnonCart(request)
        cart_products = cart.get_products()
        total = cart.total()
    else:
        customer = request.user.customer
        # Get CartProducts
        cart_products = CartProduct.objects.filter(cart=customer.cart)
        total = customer.cart.total

    return render(
        request,
        "cart.html",
        {"cart_products": cart_products, "total": total},
    )


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

        if request.user == None or request.user.is_anonymous:
            cart = AnonCart(request)
            cart.add(product, start_date, end_date)

        else:
            request.user.customer.cart.add(product, start_date, end_date)

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(json.dumps({}), status=200, content_type="application/json")


def remove_from_cart(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        product_id = data["product_id"]

        product = Product.objects.get(pk=product_id)

        if request.user == None or request.user.is_anonymous:
            cart = AnonCart(request)
            cart.remove(product.id)
            new_price = cart.total()
        else:
            request.user.customer.cart.products.remove(product)
            new_price = request.user.customer.cart.total

    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(
        json.dumps({"new_price": new_price}),
        status=200,
        content_type="application/json",
    )


def get_cart_count(request):
    response_data = {}
    if request.user == None or request.user.is_anonymous:
        cart = AnonCart(request)
        response_data["count"] = cart.count()
    else:
        response_data["count"] = request.user.customer.cart.products.count()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def has_product(request, product_id):
    if request.user == None or request.user.is_anonymous:
        cart = AnonCart(request)
        response_data = {}
        response_data["has_product"] = cart.has_product(product_id)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {}
    response_data["has_product"] = request.user.customer.cart.products.filter(
        pk=product_id
    ).exists()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def order_summary(request):
    delivery_point = [("", "Seleccione un punto de recogida")] + [
        (delivery_point.get("name"), delivery_point.get("name"))
        for delivery_point in DeliveryPoint.objects.values()
    ]
    if request.method == "GET":
        if request.user == None or request.user.is_anonymous:
            cart = AnonCart(request)
            cart_products = cart.get_products()
            total = cart.total()

            form = EditDeliveryPointAndPaymentMethodForm(
                data={"delivery_points": delivery_point}
            )

        else:
            user = request.user
            customer = Customer.objects.get(user=user)
            cart_products = CartProduct.objects.filter(cart=customer.cart)
            total = customer.cart.total

            if customer.preferred_payment_method == None:
                customer.preferred_payment_method = PaymentMethod.objects.get_or_create(
                    payment_type="A contrareembolso"
                )[0]

            form = EditDeliveryPointAndPaymentMethodForm(
                data={
                    "delivery_points": delivery_point,
                    "preferred_delivery_method": customer.preferred_delivery_point.delivery_type
                    if customer.preferred_delivery_point
                    else None,
                    "preferred_delivery_point": customer.preferred_delivery_point,
                    "payment_method": customer.preferred_payment_method,
                },
            )

    return render(
        request,
        "order-summary.html",
        {
            "form": form,
            "cart_products": cart_products,
            "total": total,
        },
    )
