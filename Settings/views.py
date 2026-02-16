from django.shortcuts import redirect, render
from AuditTrail.models import AuditLog
from django.contrib.auth.decorators import login_required
from Products.models import Product_Category, Supplier
from django.contrib import messages
# Create your views here.


@login_required
def index(request):
    
    page_name = "settings"
    
    context = {
        "page_name": page_name,
    }
    
    return render(request, "settings/index.html", context)


def add_product_category(request):
    
    if request.GET.get('cat') is not None:
         cat = request.GET.get('cat')
         new_category = Product_Category(category=cat)
         new_category.save()
         
         messages.add_message(request, messages.SUCCESS, "Successfully added new product category.")
         
         audit = AuditLog(audit_name=request.user.username, audit_action="Added new product category.", audit_module="Settings")
         audit.save()
         
         return redirect("settings")
    else:
        messages.add_message(request, messages.ERROR, "Field cannot be empty")
        return redirect("settings")
        
def add_supplier(request):
    
    if request.GET.get('supplier') is not None:
         supplier = request.GET.get('supplier')
         new_supplier = Supplier(name=supplier)
         new_supplier.save()
         
         messages.add_message(request, messages.SUCCESS, "Successfully added new supplier.")
         
         audit = AuditLog(audit_name=request.user.username, audit_action="Added new supplier.", audit_module="Settings")
         
         audit.save()
         
         return redirect("settings")
    else:
        messages.add_message(request, messages.ERROR, "Field cannot be empty")
        return redirect("settings")