from django.db import models

Type_Choice = (
    ("Offer", "Offer"),
    ("Feature", "Feature")
)


class Slider(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='slider/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='category/')
    link = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    type = models.CharField(max_length=50, choices=Type_Choice)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='productimage')
    image = models.ImageField(upload_to='productimage/')

# Create your models here.
