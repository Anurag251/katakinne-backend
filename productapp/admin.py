from django.contrib import admin
from .models import *

admin.site.register([Slider, Category, Product, ProductImage])

# Register your models here.
