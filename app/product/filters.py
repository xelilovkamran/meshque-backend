import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte")

    category = django_filters.NumberFilter(field_name="category_id")

    ordering = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price"]
        order_by = ["price", "created_at"]
