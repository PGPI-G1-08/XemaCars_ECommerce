from django.contrib import admin

from .models import Customer, DeliveryInfo

# Register your models here.


class DeliveryInfoInline(admin.TabularInline):
    model = DeliveryInfo


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    search_fields = ("user",)

    inlines = [
        DeliveryInfoInline,
    ]


admin.site.register(Customer, CustomerAdmin)
