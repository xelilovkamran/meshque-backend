from .models import ColorVariant, SizeVariant, Category, Product, ProductImage
from .serializers import ColorVariantSerializer, ProductDetailSerializer, SizeVariantSerializer, CategorySerializer, ProductImageSerializer, ProductListSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .filters import ProductFilter

# API Views


# Color Variant Views
class ColorVariantList(generics.ListCreateAPIView):
    queryset = ColorVariant.objects.all()
    serializer_class = ColorVariantSerializer
    permission_classes = [IsAdminUser]


class ColorVariantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ColorVariant.objects.all()
    serializer_class = ColorVariantSerializer
    permission_classes = [IsAdminUser]


# Size Variant Views
class SizeVariantList(generics.ListCreateAPIView):
    queryset = SizeVariant.objects.all()
    serializer_class = SizeVariantSerializer
    permission_classes = [IsAdminUser]


class SizeVariantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SizeVariant.objects.all()
    serializer_class = SizeVariantSerializer
    permission_classes = [IsAdminUser]


# Category Views
class CategorytList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


# Product Image Views
class ProductImageList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class ProductImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


# Product Views
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
