
from django.urls import path
from .views import BasketItemDetail, BasketItemList, WishlistItemList, toggle_wishlist

urlpatterns = [
    path('items/', BasketItemList.as_view()),
    path('items/<int:pk>/', BasketItemDetail.as_view()),

    path('wishlist/items/', WishlistItemList.as_view()),
    path('wishlist/toggle/', toggle_wishlist),
]
