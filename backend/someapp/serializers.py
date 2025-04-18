from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users, Author, Book, Favorite
from rest_framework.serializers import ModelSerializer


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())  # Используем ID автора

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'publish_year', 'author', 'genre', 'file']


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'biography', 'birth_year', 'books']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())  # Используем PrimaryKeyRelatedField

    class Meta:
        model = Favorite
        fields = ['user', 'author']


class UserRegisterLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'token']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
