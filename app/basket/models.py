from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from product.models import Product, SizeVariant, ColorVariant

# Create your models here.


class Basket(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="basket"
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket(user={self.user_id})"


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="basket_items"
    )

    # Variants for this basket line
    size_variant = models.ForeignKey(
        SizeVariant,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    color_variant = models.ForeignKey(
        ColorVariant,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["basket", "product", "size_variant", "color_variant"],
                name="uniq_basket_line"
            )
        ]

    def __str__(self):
        return f"BasketItem(basket={self.basket_id}, product={self.product_id}, qty={self.quantity})"


class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist(user={self.user_id})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["wishlist", "product"],
                name="uniq_wishlist_line"
            )
        ]

    def __str__(self):
        return f"WishlistItem(wishlist={self.wishlist_id}, product={self.product_id})"
