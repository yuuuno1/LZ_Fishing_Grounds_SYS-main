from django import forms
from .models import Products, Supplier, DisposeLog
from django.core.exceptions import ValidationError



class ProductCreationForm(forms.ModelForm):
    description = forms.CharField(required=False)
    scientific_name = forms.CharField(required=False)
    id = forms.HiddenInput()
    
    class Meta:
        model = Products
        fields = ("name", "category", "sub_category", "price", "stocks", "description", "scientific_name", "is_available", "product_img")
        
        
class ProductChangeForm(forms.ModelForm):
    description = forms.CharField(required=False)
    scientific_name = forms.CharField(required=False)
    
    class Meta:
        model = Products
        fields = ("name", "category", "sub_category", "price", "description", "scientific_name", "is_available", "product_img")
        

class AddStockForm(forms.Form):
    SUPPLIER_CHOICE = Supplier.objects.all()
    
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    stocks_added = forms.IntegerField(required=True, min_value=1)
    total_cost = forms.DecimalField(min_value=1, max_value=9999999, required=False)
    
    
class DisposeStockForm(forms.Form):
    
    stocks_to_dispose = forms.IntegerField(required=True, min_value=1)
    reason = forms.CharField(required=True)
        

        
    
        

    

    

