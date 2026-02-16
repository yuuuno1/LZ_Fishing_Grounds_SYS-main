from django.db import models
from django.core.validators import MinValueValidator
from users.models import *

class Product_Category(models.Model):
    category = models.CharField(max_length=50, null=False)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category
    
    
class Products(models.Model):
    
    name = models.CharField(max_length=60, null=False, unique=True)
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=40, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    stocks = models.PositiveIntegerField(null=False)
    description = models.CharField(max_length=255, null=True)
    scientific_name = models.CharField(max_length=100, null=True)
    is_available = models.BooleanField(null=False, default=1)
    product_img = models.ImageField(upload_to='products', default='lz_fishing.jpg')
    date_registered = models.DateField(null=True, auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def formatted_price(self):
        formatted = "{:,}".format(self.price)
        return formatted
    
    
class Supplier(models.Model):

    name = models.CharField(max_length=200, null=False, unique=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class StocksLog(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    stocks_added = models.PositiveIntegerField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.product_id)
    
    def formatted_cost(self):
        formatted = "{:,}".format(self.total_cost)
        return formatted
    
    
class DisposeLog(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    dispose = models.PositiveIntegerField(null=False)
    reason = models.TextField(null=False)
    date_disposed = models.DateTimeField(auto_now_add=True)
    disposed_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return str(self.product.name)
    
    

    
    



