from django.shortcuts import render, redirect
from .models import OrderProduct, Order

# Create your views here.


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
