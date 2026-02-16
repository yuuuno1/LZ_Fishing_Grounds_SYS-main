from django.db import models
from users.models import *
from Products.models import *
# Create your models here.

class Cart(models.Model):

    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    
    def __str__(self):
        return self.customer.email
    
    
class Item(models.Model):
    
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    
    def price(self):
        price = self.quantity * self.product.price
        return price
    
    def formatted_price(self):
        price = self.quantity * self.product.price
        formatted = "{:,}".format(price)
        return formatted
    
    def __str__(self):
        return self.product.name
    
    
class FeaturedProduct(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name
    
    
class Reservation(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reservedAt = models.DateTimeField(auto_now_add=True)
    gcash = models.CharField(max_length=11, null=False)
    screenshot = models.ImageField(upload_to='screenshots', null=False)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=50, null=False)
    
    def formatted_total(self):
        formatted = "{:,}".format(self.total)
        return formatted
    
    

class ShopDetails(models.Model):
    email = models.EmailField(max_length=254, null=False)
    address = models.TextField(max_length=250, null=False)
    gcash = models.CharField(max_length=50, null=False)
    facebook_url = models.URLField(max_length=200, null=False)
    phone_number = models.CharField(max_length=50, null=False)
    gcash_insta_pay = models.ImageField(upload_to='screenshot', null=True)
    

