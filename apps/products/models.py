from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    year = models.IntegerField()

    COMBUSTION_TYPES = (
        ("Gasolina", "Gasolina"),
        ("Diesel", "Diesel"),
        ("Híbrido", "Híbrido"),
        ("Eléctrico", "Eléctrico"),
    )
    combustion_type = models.CharField(max_length=255, choices=COMBUSTION_TYPES)

    description = models.TextField()

    price = models.FloatField()
    image_url = models.CharField(max_length=2083)

    # To prevent products from being deleted if they are in an order
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DeliveryPoint(models.Model):
    DELIVERY_TYPES = (
        ("Recogida en Parking", "Recogida en Parking"),
        ("Recogida en tienda", "Recogida en tienda"),
    )

    delivery_type = models.CharField(max_length=255, choices=DELIVERY_TYPES)
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name
