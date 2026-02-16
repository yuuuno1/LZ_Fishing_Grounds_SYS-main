from django.db import models
from Products.models import Products
from django.db.models import Sum


# Create your models here.
class Cart(models.Model):

    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, null=False)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(null=False)
    
    
    def __str__(self):
        return str(self.product_id)
    
    def formatted_subtotal(self):
        formatted = "{:,}".format(self.subtotal)
        return formatted
    
    
class Transaction(models.Model):
    
    total = models.DecimalField(max_digits=9, decimal_places=2)
    change  = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    date_occured = models.DateField(auto_now=True)
    cashier = models.CharField(max_length=50, null=False)
    payment_method = models.CharField(max_length=50, null=True)
    payment = models.DecimalField(max_digits=9, decimal_places=2, null=True, default=0)
    gcash_num = models.CharField(max_length=50, null=True)
    ref = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=False, default="pending")
    
    
    def formatted_total(self):
        formatted = "{:,}".format(self.total)
        return formatted
    
    def formatted_change(self):
        formatted = 0
        if self.change is not None:
            formatted = "{:,}".format(self.change)
        else:
            formatted = "0.00"
        return formatted
    
    def formatted_payment(self):
        formatted = "{:,}".format(self.payment)
        return formatted
    
    def __str__(self):
        return "Transaction ID: " + str(self.id)
    
class Item(models.Model):
    
    tnum = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(null=False)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    
    
    def __str__(self):
        return str(self.tnum)
    
    def formatted_subtotal(self):
        
        subtotal = self.objects.aggregate(Sum('subotal'))['subotal__sum']
        formatted = "{:,.2f}".format(subtotal)
        return formatted
    
