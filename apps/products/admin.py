from django.contrib import admin

from .models import DeliveryPoint, Product

# Register your models here.


class DeliveryPointAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "city", "postal_code")
    search_fields = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "image_url")
    search_fields = ("name",)


admin.site.register(DeliveryPoint, DeliveryPointAdmin)
admin.site.register(Product, ProductAdmin)
