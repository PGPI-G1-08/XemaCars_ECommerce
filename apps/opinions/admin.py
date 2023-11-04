from django.contrib import admin

# Register your models here.
from .models import Claim, Opinion


class OpinionAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "product",
        "title",
        "rating",
    )
    search_fields = (
        "customer",
        "product",
    )


class ClaimAdmin(admin.ModelAdmin):
    list_display = ("customer", "title", "resolved")
    search_fields = (
        "customer",
        "resolved",
    )


admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Claim, ClaimAdmin)
