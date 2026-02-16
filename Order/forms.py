from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['total', 'gcash_num', 'receipt']
        widgets = {
            "total": forms.HiddenInput(),
            'gcash_num': forms.TextInput(attrs={
                'type': 'text', 'minlength': '11', 'onkeypress':"return /[0-9]/i.test(event.key)",
                
            })
        }

