from django.db import models

# Create your models here.


class Complaint(models.Model):
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [("abierto", "Abierto"), ("cerrado_solucionado", "Cerrado")]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Abierto")

    def __str__(self):
        return self.title
