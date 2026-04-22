from django.db import models


# 🔹 CATEGORY CHOICES
CATEGORY_CHOICES = (
    ('phone', 'Phone'),
    ('laptop', 'Laptop'),
    ('accessory', 'Accessory'),
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)

    price = models.FloatField()
    old_price = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    stock = models.IntegerField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='phone'
    )

    def __str__(self):
        return self.name

    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


# 🔥 NEW MODEL (VERY IMPORTANT)
# 👉 Handles condition + storage + price variations
class ProductVariant(models.Model):
    CONDITION_CHOICES = (
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Superb', 'Superb'),
    )

    STORAGE_CHOICES = (
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    storage = models.CharField(max_length=50, choices=STORAGE_CHOICES)

    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.condition} - {self.storage}"


# 🔹 MULTIPLE IMAGES
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"