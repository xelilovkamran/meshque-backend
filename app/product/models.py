from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Category(models.Model):
    name_az = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    def __str__(self):
        return self.name_az


class SizeVariant(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size


class ColorVariant(models.Model):
    color_az = models.CharField(max_length=50)
    color_en = models.CharField(max_length=50)
    color_ru = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.color_az


class Product(models.Model):
    name_az = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    note_az = models.TextField(blank=True, null=True)
    note_en = models.TextField(blank=True, null=True)
    note_ru = models.TextField(blank=True, null=True)

    description_az = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    size_variants = models.ManyToManyField(
        SizeVariant, related_name='products', blank=True)
    color_variants = models.ManyToManyField(
        ColorVariant, related_name='products', blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)

    def is_new(self):
        new_threshold = timedelta(days=30)

        threshold_date = timezone.now() - new_threshold

        return self.created_at >= threshold_date

    def __str__(self):
        return self.name_az


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.name_az if self.product else "Unassigned Image"
