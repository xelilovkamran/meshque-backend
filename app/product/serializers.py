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
    # READ
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

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = ["size_variant_ids",
                        "color_variant_ids", "category_id", "uploaded_images"]

    @transaction.atomic
    def create(self, validated_data):
        size_variants = validated_data.pop("size_variant_ids", [])
        color_variants = validated_data.pop("color_variant_ids", [])
        uploaded_images = validated_data.pop("uploaded_images", [])

        product = Product.objects.create(**validated_data)

        if size_variants:
            product.size_variants.set(size_variants)

        if color_variants:
            product.color_variants.set(color_variants)

        if uploaded_images:
            ProductImage.objects.bulk_create(
                [ProductImage(product=product, image=img)
                 for img in uploaded_images]
            )

        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        size_variants = validated_data.pop("size_variant_ids", [])
        color_variants = validated_data.pop("color_variant_ids", [])
        uploaded_images = validated_data.pop("uploaded_images", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if size_variants is not None:
            instance.size_variants.set(size_variants)

        if color_variants is not None:
            instance.color_variants.set(color_variants)

        if uploaded_images is not None and len(uploaded_images) > 0:
            ProductImage.objects.bulk_create(
                [ProductImage(product=instance, image=img)
                 for img in uploaded_images]
            )

        return instance


class ProductListSerializer(ProductBaseSerializer):
    pass


class ProductDetailSerializer(ProductBaseSerializer):
    pass
