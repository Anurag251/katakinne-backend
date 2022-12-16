from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('product', ProductRUDViewSet, basename='product')
router.register('productimage', ProductImageRUDViewSet,
                basename='productimage')
router.register('category', CategoryRUDViewSet,
                basename='category')

urlpatterns = [
    path('productrud/', include(router.urls)),
    path('slider/', SliderView.as_view(), name='slider'),
    path('category/', CategoryView.as_view(), name='category'),
    path('product/', ProductView.as_view(), name='product'),
    path('addproductimage/', AddProductImage.as_view(), name='addproductimage'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]
