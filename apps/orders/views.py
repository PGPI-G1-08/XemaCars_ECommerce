from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.orders.models import OrderProduct
from apps.users.models import Customer
from apps.products.models import DeliveryPoint, Product
from apps.payments.models import PaymentMethod
from django.core.exceptions import ValidationError
import json
from django.shortcuts import redirect
from django.shortcuts import render, redirect

from .forms import FilterOrders
from django.views.generic import TemplateView

@login_required(login_url="/signin")
def add_order(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        customer = request.user.customer
        delivery_point = data["delivery_point"]
        payment_method = data["payment_method"]
        cart_products = list(map(lambda p: p["fields"], data["products"]))

        delivery_point = DeliveryPoint.objects.get(name=delivery_point)
        payment_method = PaymentMethod.objects.get(payment_type=payment_method, customer=customer)


        order = Order.objects.create(
            customer=customer,
            delivery_point=delivery_point,
            payment_form=payment_method,
        )

        for p in cart_products:
            product = Product.objects.get(id=p["product"])
            customer.cart.products.remove(product)
            order_product = OrderProduct.objects.create(
                order=order,
                product=product,
                start_date=p["start_date"],
                end_date=p["end_date"],
            )
            order_product.save()

        order.save()

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(json.dumps({"order_id": order.id}), status=200, content_type="application/json")

class AdminOrdersView(TemplateView):
    def get(self, request):
        if request.user.is_superuser:
            form = FilterOrders()
            orders = Order.objects.all()
            for order in orders:
                order.order_products = OrderProduct.objects.filter(order=order)
            return render(request, "all-orders.html", {"orders": orders, "form": form})
        else:
            return render(request, "forbidden.html")
    
    def post(self, request):
        form = FilterOrders(request.POST)
        if form.is_valid():
            only_active = form.cleaned_data["no_cancelados"]
            if only_active is True:
                orders = [order_product.order for order_product in OrderProduct.objects.all() if order_product.cancelled != only_active]
                for order in orders:
                    order.order_products = OrderProduct.objects.filter(order=order)
            else:
                orders = Order.objects.all()
            if form.cleaned_data["estado"]:
                status = form.cleaned_data["estado"]
                orders = [order_product.order for order_product in OrderProduct.objects.all() if status.lower() in order_product.status.lower()]
                for order in orders:
                    order.order_products = OrderProduct.objects.filter(order=order)
        else:
            orders = Order.objects.all()

        return render(
            request, "all-orders.html", {"orders": orders, "form": form}
        )

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
        order.order_products = OrderProduct.objects.filter(order=order).order_by(
            "id"
        )
    return render(request, "client-orders.html", {"orders": orders})
