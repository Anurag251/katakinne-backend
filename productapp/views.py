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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductRUDSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def get_queryset(self):
        if self.request.user:
            qs = Product.objects.all()
        return qs


class AddProductImage(generics.CreateAPIView):
    serializer_class = ImageofProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductImage.objects.all()

    def post(self, request):
        print(self.request.user)
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductImage.objects.all()


class CategoryRUDViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryAddSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = User.objects.get(username=username)
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password!')

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        rtoken = str(refresh)
        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'userfield': username,
            'token': token,
            'refresh_token': rtoken,
        }
        return response


class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            print(token)

            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
