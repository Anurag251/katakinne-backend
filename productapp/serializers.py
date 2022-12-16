from dataclasses import fields
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    productimage = ProductImageSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class ProductImageRUDSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=False)
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = '__all__'


class CategoryIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    link = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class ProductRUDSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.ImageField()
    tag = serializers.CharField(required=False)
    price = serializers.IntegerField()
    discount = serializers.IntegerField()
    description = serializers.CharField()
    quantity = serializers.IntegerField(required=False)
    type = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        category = validated_data.get('category_id')
        if Category.objects.filter(id=category).exists():
            category = Category.objects.get(id=category)
        else:
            raise serializers.ValidationError('Category Not Exists')
        product = Product.objects.create(category=category, **validated_data)

        return (product)


class ImageofProductSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField()
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = '__all__'


class ImageProduct(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        depth = 1


class CategoryAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.ImageField()
    link = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
        excludes = ['password']


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
