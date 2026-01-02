from rest_framework import serializers
from purchase.models import Order, OrderItem
from product.serializers import ProductBaseSerializer, SizeVariantSerializer, ColorVariantSerializer
from basket.serializers import BasketItmeProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = BasketItmeProductSerializer(read_only=True)
    size_variant = SizeVariantSerializer(read_only=True)
    color_variant = ColorVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    additional_notes = serializers.CharField(required=False, allow_blank=True)
    is_paid = serializers.BooleanField(required=False, default=False)


class OrderUpdateSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    additional_notes = serializers.CharField(required=False, allow_blank=True)
    is_paid = serializers.BooleanField(required=False, default=False)
    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES,
        required=False,
    )

    class Meta:
        model = Order
        fields = ['shipping_address', 'additional_notes', 'is_paid', 'status']
