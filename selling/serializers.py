from rest_framework import serializers
from .models import Color, SubCategory, Product, User
from djoser.serializers import UserCreateSerializer, UserSerializer


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'color_code']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'contact_number', 'roles')


