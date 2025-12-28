
from django.urls import path
from .views import UserApiView, UserDetailApiView, change_password, reset_password

urlpatterns = [
    path('users/', UserApiView.as_view()),
    path('me/', UserDetailApiView.as_view()),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_password'),
]
