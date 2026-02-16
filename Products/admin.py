from django.contrib import admin
from .models import Product_Category, Products, StocksLog, Supplier

# Register your models here.
admin.site.register({Products, StocksLog, Product_Category, Supplier})