from typing import Any
from django import forms
from django.contrib.auth import login, authenticate, logout
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class SignInForm(forms.Form):
  username = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={
      'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
      'placeholder': " ",
   
  }))
  password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput(attrs={
      'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
      'placeholder': " "
  }))
  
# Modified Registration form due to custom user model
class CustomUserCreationForm(UserCreationForm):
  token = forms.CharField(max_length=50, required=False)
   
  class Meta:
    model = CustomUser
    fields = ("first_name", "last_name", "email", "username", "token")
    
    widgets = {
        "first_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
           
        }),
        "last_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "email" : forms.EmailInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "username" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
            'minlength' : "8"
        }),
            "token" : forms.HiddenInput(attrs={
            'required': "false"
        }),
       
    }

class CustomUserChangeForm(UserChangeForm):

  class Meta:
    model = CustomUser
    fields = ("first_name", "password", "last_name", "email", "username", "role", "is_active")
    widgets = {
        "first_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
           
        }),
        "last_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "email" : forms.EmailInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "username" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
            'minlength' : "8"
        }),
        "role" : forms.Select(attrs={
            'class' : "peer h-full w-full rounded-[7px] border border-blue-gray-200 border-t-transparent bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 outline outline-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 empty:!bg-gray-900 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        }),
        "is_active" : forms.Select(attrs={
            'class' : "peer h-full w-full rounded-[7px] border border-blue-gray-200 border-t-transparent bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 outline outline-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 empty:!bg-gray-900 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        })
       
    }

class NewUserForm(UserCreationForm):
 
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "username", "role")
        widgets = {
        "first_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
           
        }),
        "last_name" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "email" : forms.EmailInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " "
        }),
        "username" : forms.TextInput(attrs={
            'class': "w-full h-full px-3 py-3 font-sans text-sm font-normal transition-all bg-transparent border rounded-md peer border-blue-gray-200 border-t-transparent text-blue-gray-700 outline outline-0 placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
            
            'placeholder': " ",
            'minlength' : "8"
        }),
        "role" : forms.Select(attrs={
            'class' : "peer h-full w-full rounded-[7px] border border-blue-gray-200 border-t-transparent bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 outline outline-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 empty:!bg-gray-900 focus:border-2 focus:border-gray-900 focus:border-t-transparent focus:outline-0 disabled:border-0 disabled:bg-blue-gray-50",
        })

    }
        
      
      
class ForgotPassForm(forms.Form):
   email = forms.EmailField(required=True)

   def clean(self):
      email = self.cleaned_data["email"]
      users = CustomUser.objects.filter(email=email)
      
      if len(users) == 0:
          raise ValidationError('Email is not associated to any account.')
      
      
      
class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    
    re_password = forms.CharField(
        widget=forms.PasswordInput,
        
    )
    
        
    def clean(self):
       password = self.cleaned_data['password']
       re_password = self.cleaned_data['re_password']
       
       if password != re_password:
           raise ValidationError('Passwords do not match.')
       
       


          
      
      
      
