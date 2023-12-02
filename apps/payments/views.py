from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import stripe

from apps.users.models import Customer


@login_required(login_url="/signin")
def delete(request, payment_method_id):
    user = request.user
    customer = Customer.objects.get(user=user)
    payment_methods = customer.get_stripe_payment_methods()

    for payment_method in payment_methods:
        if payment_method.id == payment_method_id:
            stripe.PaymentMethod.detach(payment_method.id)
            return redirect("/payment-methods")
