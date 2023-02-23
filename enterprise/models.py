from django.db import models


class Product(models.Model):
    # Blank = True means that the field is not required
    # Null = True means that the field can be empty in the database
    image = models.ImageField(upload_to="static/images/products", blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        has_stock = self.stock_quantity > 0

        if has_stock:
            self.stock_quantity -= 1
            self.save()
            return None

        super().delete(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
