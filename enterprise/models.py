from django.db import models


class Product(models.Model):
    # Blank = True means that the field is not required
    # Null = True means that the field can be empty in the database
    image = models.ImageField(upload_to="static/images/products", blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.stock_quantity - 1 <= 0:
            super().delete(*args, **kwargs)

        self.stock_quantity -= 1
        self.save()

    # Sort by product quantity, descending
    class Meta:
        ordering = ["-stock_quantity"]


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()
    # This field is not required because it will be calculated, not filled by the user
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
