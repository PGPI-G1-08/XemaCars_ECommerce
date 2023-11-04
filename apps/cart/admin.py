from django.contrib import admin

# Register your models here.
# Include the cart model in the admin site, so that we can also add and view the products in the cart within the cart details and creation pages.
from .models import Cart, CartProduct


class CartProductInline(admin.TabularInline):
    model = CartProduct


class CartAdmin(admin.ModelAdmin):
    list_display = ()
    search_fields = ()

    inlines = [
        CartProductInline,
    ]


admin.site.register(Cart, CartAdmin)
