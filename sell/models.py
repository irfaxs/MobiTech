from django.db import models
from django.contrib.auth.models import User

# Brand
class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/')

    def __str__(self):
        return self.name


# Model (Phone)
class Device(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='devices/')
    base_price = models.IntegerField()

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Variant(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=50)   # 6GB/64GB
    price = models.IntegerField()

    def __str__(self):
        return f"{self.device.name} - {self.name}"



class SellRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ ADD

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('pickup', 'Pickup Scheduled'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.device.name}"