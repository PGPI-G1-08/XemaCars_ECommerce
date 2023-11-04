from django.contrib import admin

from .models import Customer

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    exclude = ("cart",)
    list_display = ("user", "phone_number")
    search_fields = ("user",)


admin.site.register(Customer, CustomerAdmin)
