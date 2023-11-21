from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.users.models import Customer
from apps.products.models import DeliveryPoint, Product
from apps.payments.models import PaymentMethod
from django.core.exceptions import ValidationError
import json



@login_required(login_url="/signin")
def add_order(request):
    if request.method != "POST":
        return

    try:
        data = json.loads(request.body)

        user = request.user.customer
        delivery_point_id = data["delivery_point"]
        payment_method_id = data["payment_method"]

        delivery_point = DeliveryPoint.objects.get(pk=delivery_point_id)
        payment_method = PaymentMethod.objects.get(pk=payment_method_id)

        order = Order.objects.create(
            customer=customer,
            delivery_point=delivery_point,
            payment_method=payment_method,
        )

    except ValidationError as e:
        return HttpResponse(json.dumps({"error": e.message}), status=400)

    return HttpResponse(json.dumps({"order_id": order.id}), status=200, content_type="application/json")
