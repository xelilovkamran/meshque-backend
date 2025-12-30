from django.db import transaction
from rest_framework import serializers
from .models import ColorVariant, SizeVariant, Category, Product, ProductImage


class ColorVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'


class SizeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductBaseSerializer(serializers.ModelSerializer):
    # READ (full objects)
    size_variants = SizeVariantSerializer(many=True, read_only=True)
    color_variants = ColorVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    # WRITE (ids)
    size_variant_ids = serializers.PrimaryKeyRelatedField(
        queryset=SizeVariant.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    color_variant_ids = serializers.PrimaryKeyRelatedField(
        queryset=ColorVariant.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        required=True,
        source="category",
    )

    image_ids = serializers.PrimaryKeyRelatedField(
        queryset=ProductImage.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = [
            "size_variant_ids",
            "color_variant_ids",
            "category_id",
            "image_ids",
        ]

    @transaction.atomic
    def create(self, validated_data):
        size_variants = validated_data.pop("size_variant_ids", [])
        color_variants = validated_data.pop("color_variant_ids", [])
        images = validated_data.pop("image_ids", [])
        print("images:", images)

        product = Product.objects.create(**validated_data)

        if size_variants:
            product.size_variants.set(size_variants)
        if color_variants:
            product.color_variants.set(color_variants)

        if images:
            ProductImage.objects.filter(
                id__in=[i.id for i in images]).update(product=product)

        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        size_variants = validated_data.pop("size_variant_ids", None)
        color_variants = validated_data.pop("color_variant_ids", None)
        images = validated_data.pop("image_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if size_variants is not None:
            instance.size_variants.set(size_variants)

        if color_variants is not None:
            instance.color_variants.set(color_variants)

        if images is not None:
            ProductImage.objects.filter(product=instance).update(product=None)
            ProductImage.objects.filter(
                id__in=[i.id for i in images]).update(product=instance)

        return instance


class ProductListSerializer(ProductBaseSerializer):
    pass


class ProductDetailSerializer(ProductBaseSerializer):
    pass
