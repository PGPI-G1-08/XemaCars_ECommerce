from django.contrib import admin

from .models import PaymentMethod


# Register your models here.
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("payment_type",)
    search_fields = ("payment_type",)


admin.site.register(PaymentMethod, PaymentMethodAdmin)
