from django.db import models
from django.conf import settings
from product.models import Product, SizeVariant, ColorVariant

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Hazırlanır'),
        ('Delivered', 'Təslim edildi'),
        ('Cancelled', 'Ləğv edildi'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Processing')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    additional_notes = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    size_variant = models.ForeignKey(
        SizeVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')

    color_variant = models.ForeignKey(
        ColorVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.id}"
