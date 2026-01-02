from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from purchase.models import Order
from basket.models import Basket
from .serializers import OrderCreateSerializer, OrderListSerializer, OrderUpdateSerializer
from .filters import OrderFilter


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderListSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        try:
            basket = Basket.objects.get(user=user)
        except Basket.DoesNotExist:
            return Response({"error": "Basket not found"}, status=status.HTTP_404_NOT_FOUND)

        basket_items = basket.items.select_related(
            "product", "size_variant", "color_variant")
        if not basket_items.exists():
            return Response({"error": "Basket is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        for item in basket_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"message": f"Product {item.product.name} has insufficient stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            total_price += item.product.discounted_price() * item.quantity

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            shipping_address=data.get("shipping_address", ""),
            additional_notes=data.get("additional_notes", ""),
            is_paid=data.get("is_paid", False),
        )

        for item in basket_items:
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price_per_item=item.product.discounted_price(),
                size_variant=item.size_variant,
                color_variant=item.color_variant,
            )

        basket.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(
            {"message": "Order created", "order": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return OrderUpdateSerializer
        return OrderListSerializer
