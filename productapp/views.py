from rest_framework.response import Response
from rest_framework import (
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.views import APIView
from .models import *
from .serializers import *
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.db.models import CharField, Value, IntegerField, Q
# Create your views here.


class SliderView(generics.ListAPIView):
    serializer_class = SliderSerializer
    permission_classes = ([permissions.AllowAny,])
    authenticated_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Slider.objects.all()


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = ([permissions.AllowAny,])
    authenticated_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.all()


class ProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = ([permissions.AllowAny,])
    authenticated_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.all()
        query = self.request.GET.get("user_data")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(tag__icontains=query) |
                Q(type__icontains=query) |
                Q(category__name__icontains=query) |
                Q(date__icontains=query)
            ).distinct()
        return qs


class ProductRUDViewSet(viewsets.ModelViewSet):
    serializer_class = ProductRUDSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()


class AddProductImage(generics.CreateAPIView):
    serializer_class = ImageofProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProductImage.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = request.data
        print(data.get('product'))
        serializer.is_valid(raise_exception=True)
        if Product.objects.filter(id=data.get('product')).exists():
            product_item = Product.objects.get(id=data.get('product'))
        else:
            raise serializers.ValidationError('Product Not Exists')
        images = data.getlist('image')
        for image in images:
            ProductImage.objects.create(product=product_item, image=image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductImageRUDViewSet(viewsets.ModelViewSet):
    serializer_class = ImageProduct
    permission_classes = [permissions.AllowAny]
    queryset = ProductImage.objects.all()
