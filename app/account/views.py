from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,  permission_classes
from drf_spectacular.utils import extend_schema


class UserApiView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request={
        "application/json": {
            "example": {
                "old_password": "current_password",
                "new_password": "new_secure_password"
            }
        }
    },
    responses={
        200: {"example": {"message": "Password changed successfully."}},
        400: {"example": {"message": "Old password is incorrect."}},
    },
)
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


@extend_schema(
    request={
        "application/json": {
            "example": {
                "email": "example@gmail.com",
                "new_password": "new_secure_password"
            }
        }
    },
    responses={
        200: {"example": {"message": "Password reset successfully."}},
        404: {"example": {"message": "User not found."}},
    },
)
@api_view(['POST',])
def reset_password(request):
    new_password = request.data.get('new_password')
    email = request.data.get('email')

    user = CustomUser.objects.get(email=email)

    if not user:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Set the new password
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
