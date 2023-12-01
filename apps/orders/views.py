from datetime import datetime
import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import redirect, render

from apps.orders.models import Order
from apps.orders.models import OrderProduct
from apps.payments.models import PaymentMethod
from apps.products.models import DeliveryPoint, Product
from apps.cart.anon_cart import AnonCart
from apps.cart.models import CartProduct
from .forms import SearchIdentifierOrderForm


def add_order(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        delivery_point = data["delivery_point"]
        delivery_point = DeliveryPoint.objects.get(name=delivery_point)

        payment_method = data["payment_method"]

        if request.user == None or request.user.is_anonymous:
            email = data["email"]
            if email == "":
                raise ValidationError("Debe ingresar un email")
            if payment_method == "A contrareembolso":
                payment_method = PaymentMethod.objects.get_or_create(
                    payment_type=payment_method
                )[0]
            else:
                # TODO
                pass

            order = Order.objects.create(
                email=email,
                delivery_point=delivery_point,
                payment_form=payment_method,
            )

            cart = AnonCart(request)
            cart_copy = cart.cart.copy()
            for p in cart_copy:
                product = Product.objects.get(id=p)
                start_date = datetime.strptime(
                    cart.cart[p]["start_date"], "%Y-%m-%d"
                ).date()
                end_date = datetime.strptime(
                    cart.cart[p]["end_date"], "%Y-%m-%d"
                ).date()

                cart.remove(p)

                order_product = OrderProduct.objects.create(
                    order=order,
                    product=product,
                    start_date=start_date,
                    end_date=end_date,
                )
                order_product.save()

            order.save()

        else:
            customer = request.user.customer
            if payment_method == "A contrareembolso":
                payment_method = PaymentMethod.objects.get_or_create(
                    payment_type=payment_method
                )[0]
            else:
                payment_method = PaymentMethod.objects.get(
                    payment_type=payment_method, customer=customer
                )

            order = Order.objects.create(
                customer=customer,
                delivery_point=delivery_point,
                payment_form=payment_method,
            )

            cart_products = CartProduct.objects.filter(cart=customer.cart)
            for p in cart_products:
                product = Product.objects.get(id=p.product.id)
                customer.cart.products.remove(product)
                order_product = OrderProduct.objects.create(
                    order=order,
                    product=product,
                    start_date=p.start_date,
                    end_date=p.end_date,
                )
                order_product.save()

            order.save()

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(
        json.dumps({"order_id": order.id}), status=200, content_type="application/json"
    )


def search_order(request):
    form = SearchIdentifierOrderForm(request.POST)
    if form.is_valid() and form.cleaned_data["identifier"] != "":
        order = Order.objects.filter(identifier=form.cleaned_data["identifier"])
        if not order:
            return redirect("search_order")
        else:
            order = order[0].identifier.replace(" ", "")
            return redirect("my_order_detail", order)

    return render(request, "search-order.html", {"form": form})


def my_order_detail(request, order_identifier):
    order_identifier = " ".join(
        order_identifier[i : i + 5] for i in range(0, len(order_identifier), 5)
    )
    try:
        order = Order.objects.get(identifier=order_identifier)
    except Order.DoesNotExist:
        return redirect("search_order")

    order.order_products = OrderProduct.objects.filter(order=order).order_by("id")

    return render(request, "order-detail.html", {"order": order})


def my_orders(request):
    if request.user.is_anonymous:
        return redirect("login")

    form = SearchIdentifierOrderForm(request.POST)
    customer = request.user.customer
    if form.is_valid() and form.cleaned_data["identifier"] != "":
        orders = (
            Order.objects.filter(customer=customer)
            .filter(identifier=form.cleaned_data["identifier"])
            .order_by("-date")
        )
        if not orders:
            return redirect("my_orders")
    else:
        orders = Order.objects.filter(customer=customer).order_by("-date")

    if orders:
        for order in orders:
            order.order_products = OrderProduct.objects.filter(order=order).order_by(
                "id"
            )

    return render(request, "orders.html", {"orders": orders, "form": form})


def all_orders(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
        for order in orders:
            order.order_products = OrderProduct.objects.filter(order=order).order_by(
                "id"
            )
        return render(request, "all-orders.html", {"orders": orders})
    else:
        return render(request, "forbidden.html")


def cancel_orderproduct(request, orderproduct_id):
    if request.user.is_superuser:
        orderproduct = OrderProduct.objects.get(id=orderproduct_id)
        orderproduct.cancelled = True
        orderproduct.save()
        return redirect("all-orders")
    else:
        return render(request, "forbidden.html")


def cancel_order(request, order_id):
    if request.user.is_superuser:
        order = Order.objects.get(id=order_id)
        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:
            order_product.cancelled = True
            order_product.save()
        order.cancelled = True
        order.save()
        return redirect("all-orders")
    else:
        return render(request, "forbidden.html")
