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

import stripe

from django.core.mail import send_mail


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
                payment_method = PaymentMethod.objects.get_or_create(
                    payment_type=payment_method
                )[0]
                handle_payment(request)

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
                payment_method = PaymentMethod.objects.get_or_create(
                    payment_type=payment_method
                )[0]
                handle_payment(request)

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

            email = request.user.email

            order.save()

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    send_mail_after_order(order, email)

    return HttpResponse(
        json.dumps({"order_id": order.id}), status=200, content_type="application/json"
    )


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


def handle_payment(request):
    data = json.loads(request.body)
    client_secret = data["client_secret"]
    intent_id = client_secret.split("_secret")[0]
    intent = stripe.PaymentIntent.retrieve(intent_id)

    status = intent["status"]
    if status == "succeeded":
        return
    elif status == "requires_payment_method":
        raise ValidationError("El pago no ha sido completado")
    else:
        raise ValidationError("El pago no ha sido completado")


def send_mail_after_order(order, email):
    products = OrderProduct.objects.filter(order=order)
    subject = "XemaCars - Orden de compra"
    message = f"""
    Gracias por tu compra!
    Detalle de la orden:

    """

    for product in products:
        message += f"""
        Producto: {product.product.name}
        Fecha de inicio: {product.start_date}
        Fecha de fin: {product.end_date}

        """
    message += f"""
    Punto de entrega: {order.delivery_point.name}
    """

    message += f"""
    Metodo de pago: {order.payment_form.payment_type}
    """

    message += f"""
    Total: {order.total} €
    """

    message += f"""

    Numero de orden: {order.id}

    """

    message += f"""
    Para cualquier consulta, comunicate con nosotros a traves de correo electronico a "xemacars.nrply@outlook.es",
    """

    # Send email
    send_mail(
        subject,
        message,
        "xemacars.nrply@outlook.es",
        [email],
        fail_silently=False,
    )
