from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from .models import Basket, BasketItem, Wishlist, WishlistItem
from .serializers import BasketItemListSerializer, BasketItemDetailSerializer, WishlistItemSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view,  permission_classes
from drf_spectacular.utils import extend_schema

# API Views


class BasketItemList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketItemListSerializer

    def get(self, request):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        items = basket.items.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]

        serializer = self.serializer_class(
            data=request.data)
        if serializer.is_valid():
            serializer.save(basket=basket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasketItemDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemDetailSerializer
    permission_classes = [IsAuthenticated]


class WishlistItemList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wishlist = Wishlist.objects.get_or_create(user=user)[0]
        items = wishlist.items.all()
        serializer = WishlistItemSerializer(items, many=True)
        return Response(serializer.data)


@extend_schema(
    request={
        "application/json": {
            "example": {
                "product_id": 1
            }
        }
    },
    responses={
        201: {"example": {"message": "Product added to wishlist."}},
        200: {"example": {"message": "Product removed from wishlist."}},
        400: {"example": {"message": "Product ID is required."}},
        404: {"example": {"message": "Product not found."}},
    },
)
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def toggle_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.get_or_create(user=user)[0]

    product_id = request.data.get('product_id')
    if not product_id:
        return Response({'message': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    wishlist_item, item_created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    if not item_created:
        wishlist_item.delete()
        return Response({'message': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)

    return Response({'message': 'Product added to wishlist.'}, status=status.HTTP_201_CREATED)
