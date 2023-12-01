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

import json

from .forms import FilterOrders
from django.views.generic import TemplateView

from apps.products.models import DeliveryPoint, Product
from apps.cart.anon_cart import AnonCart
from apps.cart.models import CartProduct


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


class AdminOrdersView(TemplateView):
    def get(self, request):
        if request.user.is_superuser:
            form = FilterOrders()
            orders = Order.objects.all().order_by("-date")
            for order in orders:
                order.order_products = OrderProduct.objects.filter(order=order)
            return render(request, "all-orders.html", {"orders": orders, "form": form})
        else:
            return render(request, "forbidden.html")

    def post(self, request):
        form = FilterOrders(request.POST)
        if form.is_valid():
            only_active = form.cleaned_data["no_cancelados"]
            status = form.cleaned_data["status"]
            customer = form.cleaned_data["customer"]
            orders = Order.objects.all().order_by("-date")
            if only_active:
                orders = [order for order in orders if not order.completely_cancelled]
            if customer != "":
                # Check for username, email and order emails
                orders = [
                    order
                    for order in orders
                    if (
                        order.customer is not None
                        and (
                            customer.lower() in order.customer.user.username.lower()
                            or customer.lower() in order.customer.user.email.lower()
                        )
                    )
                    or (
                        order.email is not None
                        and customer.lower() in order.email.lower()
                    )
                ]
            if status != "Todos":
                orders = [
                    order
                    for order in orders
                    if any(
                        status.lower() in op.status.lower()
                        for op in order.orderproduct_set.all()
                    )
                ]
        else:
            orders = Order.objects.all().order_by("-date")

        for order in orders:
            order.order_products = OrderProduct.objects.filter(order=order)
        return render(request, "all-orders.html", {"orders": orders, "form": form})


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


def client_orders(request, pk):
    orders = Order.objects.get(Customer, pk=pk)
    for order in orders:
        order.order_products = OrderProduct.objects.filter(order=order).order_by("id")
    return render(request, "client-orders.html", {"orders": orders})
