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
