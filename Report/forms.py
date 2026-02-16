from django import forms


class UserReportForm(forms.Form):
    
    ROLE_CHOICES = {
        "All": "All",
       "Admin": "Admin", 
       "Staff": "Admin", 
       "Customer": "Customer", 
    }
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=False)
    
    


    
    
