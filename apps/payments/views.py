from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import stripe

from apps.users.models import Customer


@login_required(login_url="/signin")
def delete(request, payment_method_id):
    user = request.user
    customer = Customer.objects.get(user=user)
    stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
    payment_methods = stripe.PaymentMethod.list(
        customer=stripe_customer.id, type="card"
    )

    for payment_method in payment_methods:
        if payment_method.id == payment_method_id:
            stripe.PaymentMethod.detach(payment_method.id)
            return redirect("/payment-methods")
