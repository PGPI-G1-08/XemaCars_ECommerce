from django.contrib import admin

from .models import Customer
from apps.payments.models import PaymentMethod

# Register your models here.


class PaymentMethodInline(admin.StackedInline):
    model = PaymentMethod
    extra = 1


class CustomerAdmin(admin.ModelAdmin):
    inlines = [PaymentMethodInline]
    exclude = ("cart",)
    list_display = ("user", "phone_number")
    search_fields = ("user",)


admin.site.register(Customer, CustomerAdmin)
