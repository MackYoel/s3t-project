from django.db import models
from accounts.models import Person


class Product(models.Model):
    provider = models.ForeignKey(Person)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='/images')
    size = models.CharField(max_length=50)
    price = models.FloatField()
    available = models.BooleanField(default=True, blank=True)


# class ProductColor:
#     product
#     color


# class Color:
#     name


# class Order:
#     ordered_at
#     provider
#     total


# class OrderDetails:
#     order
#     product_color
#     dozen_quantity
#     subtotal
