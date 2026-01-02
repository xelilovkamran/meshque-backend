
from django.urls import path
from .views import OrderList, OrderDetail

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
]
