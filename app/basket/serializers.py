from rest_framework import serializers
from product.models import ColorVariant, SizeVariant, Product
from product.serializers import ColorVariantSerializer, SizeVariantSerializer
from .models import BasketItem, WishlistItem
from django.db import transaction


class BasketItmeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_az', 'name_en', 'name_ru', 'price']


class BasketItemBaseSerializer(serializers.ModelSerializer):
    # Nested read-only serializers for variants
    size_variant = SizeVariantSerializer(read_only=True)
    color_variant = ColorVariantSerializer(read_only=True)

    # Write-only fields for variant IDs
    size_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=SizeVariant.objects.all(),
        source='size_variant',
        write_only=True,
        required=True,
        allow_null=False,
    )
    color_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ColorVariant.objects.all(),
        source='color_variant',
        write_only=True,
        required=True,
        allow_null=False,
    )

    class Meta:
        model = BasketItem
        exclude = ['basket']

    @transaction.atomic
    def create(self, validated_data):
        size_variant = validated_data.pop("size_variant", None)
        color_variant = validated_data.pop("color_variant", None)
        quantity = validated_data.pop("quantity", 1)
        product = validated_data.pop("product")
        basket = validated_data.pop("basket")

        item = BasketItem.objects.select_for_update().filter(
            basket=basket,
            product=product,
            size_variant=size_variant,
            color_variant=color_variant,
        ).first()

        if item:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
            return item

        return BasketItem.objects.create(
            basket=basket,
            product=product,
            size_variant=size_variant,
            color_variant=color_variant,
            quantity=quantity,
            **validated_data,
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class BasketItemListSerializer(BasketItemBaseSerializer):
    product = BasketItmeProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )


class BasketItemDetailSerializer(BasketItemBaseSerializer):
    pass


class WishlistItemSerializer(serializers.ModelSerializer):
    product = BasketItmeProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'created_at']
