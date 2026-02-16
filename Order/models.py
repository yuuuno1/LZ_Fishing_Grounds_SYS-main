from django.db import models
from Products.models import *
from users.models import CustomUser
# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=9, decimal_places=2, null=True, default=0)
    date_occured = models.DateField(auto_now=True)
    gcash_num = models.CharField(max_length=11, null=False)
    receipt = models.ImageField(upload_to='screenshot_receipt')
    status = models.CharField(max_length=50, default="pending")
    
    
    def __str__(self):
        return str(self.id)
    
    
    def formatted_total(self):
        total = self.total
        formatted = "{:,}".format(total)
        return formatted
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
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
    

    
