from .anon_cart import AnonCart


def cart(request):
    return {"cart": AnonCart(request)}
