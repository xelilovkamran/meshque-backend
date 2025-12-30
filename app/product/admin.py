from django.contrib import admin
from .models import Category, SizeVariant, ColorVariant, Product, ProductImage

# Register your models here.

admin.site.register(Category)
admin.site.register(SizeVariant)
admin.site.register(ColorVariant)
admin.site.register(Product)
admin.site.register(ProductImage)
