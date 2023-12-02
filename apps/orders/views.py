from datetime import datetime
import json
from django.conf import settings

from django.core.exceptions import ValidationError
from django.http import HttpResponse
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
from .forms import SearchIdentifierOrderForm

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
    Para cualquier consulta, comunicate con nosotros a traves de correo electronico a "contacto@xemacars.com",
    """

    # Send email
    send_mail(
        subject,
        message,
        settings.EMAIL_FROM,
        [email],
        fail_silently=False,
    )


def create_payment_intent(request):
    data = json.loads(request.body)
    if request.user == None or request.user.is_anonymous:
        cart = AnonCart(request)
        total = cart.total()
    else:
        customer = request.user.customer
        total = customer.cart.total

    # try:
    if request.user == None or request.user.is_anonymous:
        intent = stripe.PaymentIntent.create(
            # total is multiplied by 100 because stripe works with cents
            amount=int(total) * 100,
            currency="eur",
        )
    else:
        if request.user.customer.stripe_customer_id == None:
            request.user.customer.stripe_customer_id = stripe.Customer.create(
                email=request.user.email
            ).id
            request.user.customer.save()

        save_card = data["save_card"]
        payment_method = data["payment_method"]

        # Check if the selected payment method is in the customer's payment methods
        payment_methods = request.user.customer.get_stripe_payment_methods()
        valid_payment_method = False
        if payment_method != "Nueva Tarjeta":
            for pm in payment_methods:
                if payment_method == pm.id:
                    valid_payment_method = True
                    break
        else:
            valid_payment_method = True

        if not valid_payment_method:
            return HttpResponse(
                json.dumps({"error": "Metodo de pago no encontrado"}),
                status=404,
                content_type="application/json",
            )

        off_session = save_card or payment_method != "Nueva Tarjeta"

        # If it is, create an intent
        intent = stripe.PaymentIntent.create(
            setup_future_usage="off_session" if off_session else None,
            # total is multiplied by 100 because stripe works with cents
            amount=int(total) * 100,
            currency="eur",
            customer=request.user.customer.stripe_customer_id,
            payment_method=payment_method
            if payment_method != "Nueva Tarjeta"
            else None,
            confirm=True if payment_method != "Nueva Tarjeta" else False,
            # No redirects
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never",
            }
            if payment_method != "Nueva Tarjeta"
            else {},
        )
    # except Exception as e:
    #     return HttpResponse(json.dumps({"error": e.error}), status=400)

    return HttpResponse(
        json.dumps({"client_secret": intent["client_secret"]}),
        status=200,
        content_type="application/json",
    )
