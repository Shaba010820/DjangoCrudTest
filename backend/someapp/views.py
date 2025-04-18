from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Author, Book, Favorite, Users
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    FavoriteSerializer,
    UserRegisterLoginSerializer
)
from django.views.generic import TemplateView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'someapp/index.html')


@extend_schema(tags=['Authors'])
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@extend_schema(tags=['Books'])
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(tags=['Favorites'])
class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


@extend_schema(
    request=UserRegisterLoginSerializer,
    responses={200: UserRegisterLoginSerializer, 400: 'Error'}
)
class UserRegisterLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'detail': 'User authenticated successfully!'
            }, status=status.HTTP_200_OK)

        serializer = UserRegisterLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            channel_layer = get_channel_layer()
            all_users = Users.objects.exclude(id=user.id)

            for u in all_users:
                async_to_sync(channel_layer.group_send)(
                    f"user_{u.id}",
                    {
                        'type': 'send_notification',
                        'message': f"Новый пользователь {user.username} зарегистрировался!"
                    }
                )

            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'detail': 'User registered and authenticated successfully!'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

