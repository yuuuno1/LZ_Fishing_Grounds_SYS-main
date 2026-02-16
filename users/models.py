from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
  ("staff", "Staff"),
  ("admin", "Admin"),
  ("customer", "Customer"),
  ]
STATUS_CHOICES = [
  (1, "Active"),
  (0, "Inactive"),

  ]

class CustomUser(AbstractUser):
  role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, default="customer")
  
  email = models.EmailField(unique=True)
  
  is_verified = models.BooleanField(default=False)
  
  is_active = models.BooleanField(default=True, choices=STATUS_CHOICES)
  
  token = models.CharField(max_length=50, null=True)
  
  def __str__(self):
    return self.username
  
  
  
class TipGuide(models.Model):
    
    LABEL_CHOICES = [
        ("tips", "Tips"),
        ("guides",  "Guides")
    ]
    
    
    title = models.CharField(max_length=100, null=False)
    body = models.TextField(max_length=500, null=False)
    label = models.TextField(choices=LABEL_CHOICES, null=True)
    
    def __str__(self) -> str:
        return self.title
    
class TGimages(models.Model):
    tid = models.ForeignKey(TipGuide, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="tips_guides") 
    
    def __str__(self) -> str:
        return self.tid.title