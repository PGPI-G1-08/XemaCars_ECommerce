from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from apps.products.models import Product
from .models import CartProduct

from apps.users.models import Customer
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from apps.cart.forms import EditDeliveryPointAndPaymentMethodForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from apps.products.models import DeliveryPoint
from apps.payments.models import PaymentMethod


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


@login_required(login_url="/signin")
def order_summary(request):
    delivery_point = [("", "Seleccione un punto de recogida")] + [
        (delivery_point.get("name"), delivery_point.get("name"))
        for delivery_point in DeliveryPoint.objects.values()
    ]
    form = EditDeliveryPointAndPaymentMethodForm(
        data={"delivery_points": delivery_point}
    )
    if request.method == "POST":
        form = EditDeliveryPointAndPaymentMethodForm(
            request.POST, data={"delivery_points": delivery_point}
        )
        if form.is_valid():
            user = request.user

            customer = Customer.objects.get(user=user)

            delivery_point = form.cleaned_data.get("preferred_delivery_point")
            if delivery_point:
                delivery_point = DeliveryPoint.objects.get(name=delivery_point)
                customer.preferred_delivery_point = delivery_point

            payment_method = form.cleaned_data.get("payment_method")
            if payment_method:
                payment_method = PaymentMethod.objects.create(
                    payment_type=payment_method
                )
                customer.payment_methods.set([payment_method])
            customer.save()

            return redirect("/")
    if request.method == "GET":
        user = request.user
        customer = Customer.objects.get(user=user)
        cart_products = CartProduct.objects.filter(cart=customer.cart)
        form = EditDeliveryPointAndPaymentMethodForm(
            data={"delivery_points": delivery_point},
            initial={
                "preferred_delivery_point": customer.preferred_delivery_point,
                "payment_method": customer.payment_methods.first(),
            },
        )
    return render(
        request,
        "order-summary.html",
        {
            "form": form,
            "customer": customer,
            "cart_products": cart_products,
            "total": customer.cart.total,
        },
    )
