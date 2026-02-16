from django.db.models.signals import post_save, pre_delete
from users.models import CustomUser
from django.dispatch import receiver
from .models import Cart
 
 
@receiver(post_save, sender=CustomUser) 
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
 
  