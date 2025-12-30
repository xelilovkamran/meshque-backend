
from django.urls import path
from .views import ColorVariantList, ColorVariantDetail, SizeVariantList, SizeVariantDetail, CategoryDetail, CategorytList, ProductImageList, ProductImageDetail, ProductList, ProductDetail

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),

    path('sizes/', SizeVariantList.as_view()),
    path('sizes/<int:pk>/', SizeVariantDetail.as_view()),

    path('colors/', ColorVariantList.as_view()),
    path('colors/<int:pk>/', ColorVariantDetail.as_view()),

    path('categories/', CategorytList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),

    path('product-images/', ProductImageList.as_view()),
    path('product-images/<int:pk>/', ProductImageDetail.as_view()),
]
