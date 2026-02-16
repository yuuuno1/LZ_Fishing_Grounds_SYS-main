from django.shortcuts import render
from users.models import CustomUser
from Products.models import *
from PointOfSale.models import *
from Order.models import Order
from AuditTrail.models import AuditLog
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    page_name = "reports"
    user_roles = ["All", "admin", "staff", "customer"]
    categories = Product_Category.objects.all()
    products = Products.objects.all()
    suppliers = Supplier.objects.all()
     
    context = {
        'page_name': page_name,
        'user_roles': user_roles,
        'categories': categories,
        'products': products,
        'suppliers': suppliers,  
    }
    
    return render(request, "reports/index.html", context)


def user_report(request):
    users = CustomUser.objects.all()
    
    if request.method == "POST":
        role = request.POST.get('role')
        
        if role != "All":
            users = CustomUser.objects.filter(role=role)
            log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on users", audit_module="Reports")
            log.save()
            
    context = {
        "users": users,

    }
    return render(request, "reports/user_report.html", context)



def product_report(request):
    products = Products.objects.all()
    
    if request.method == "POST":
        category = request.POST.get('category')
        sub = request.POST.get('sub')
        
        
        if category != "All" and sub:
            category_obj = Product_Category.objects.get(id=category)
            products = Products.objects.filter(category=category_obj).filter(sub_category__icontains=sub)
            
        elif category == "All" and sub:
            products = Products.objects.filter(sub_category__icontains=sub)
            
        elif category != "All" and sub == "":
            category_obj = Product_Category.objects.get(id=category)
            products = Products.objects.filter(category=category_obj)
            
        log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on products", audit_module="Reports")
        log.save()
                    
    context = {
        "products": products,

    }
    return render(request, "reports/product_report.html", context)


def stockslog_report(request):
    logs = StocksLog.objects.all()
    
    if request.method == "POST":
        product = request.POST.get('product')
        supplier = request.POST.get('supplier')
        
        if product != "All":
            logs = StocksLog.objects.filter(product_id__id=product)
            
            if supplier != "All":
                logs = StocksLog.objects.filter(product_id__id=product).filter(supplier__id=supplier)
                
        elif supplier != "All":
            logs = StocksLog.objects.filter(supplier__id=supplier)
            
            if product != "All":
                logs = StocksLog.objects.filter(supplier__id=supplier).filter(product_id__id=product)
        
        log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on stock logs", audit_module="Reports")
        log.save()       
                
        
    context = {
        'logs': logs
    }
    
    return render(request, "reports/stockslog_report.html", context)
    
    
def pos_report(request):
    logs = Transaction.objects.all()
    
    if request.method == "POST":
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        
        if date_from != "":
            logs = Transaction.objects.filter(date_occured__gte=date_from)
            if date_to != "":
                logs = Transaction.objects.filter(date_occured__gte=date_from, date_occured__lte=date_to)
                
        elif date_to != "":
            logs = Transaction.objects.filter(date_occured__lte=date_to)
            if date_from != "":
                logs = Transaction.objects.filter(date_occured__gte=date_from, date_occured__lte=date_to)
                
        log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on pos sales transactions", audit_module="Reports")
        log.save()
            
    context = {
        "logs": logs,

    }
    return render(request, "reports/pos_report.html", context)


def shop_report(request):
    logs = Order.objects.all()
    
    if request.method == "POST":
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        
        if date_from != "":
            logs = Order.objects.filter(date_occured__gte=date_from)
            if date_to != "":
                logs = Order.objects.filter(date_occured__gte=date_from, date_occured__lte=date_to)
                
        elif date_to != "":
            logs = Order.objects.filter(date_occured__lte=date_to)
            if date_from != "":
                logs = Order.objects.filter(date_occured__gte=date_from, date_occured__lte=date_to)
                
    log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on e-commerce sales transactions", audit_module="Reports")
    log.save()        
            
    context = {
        "logs": logs,

    }
    return render(request, "reports/shop_report.html", context)


def audit_report(request):
    logs = AuditLog.objects.all()
    
    if request.method == "POST":
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        
        if date_from != "":
            logs = AuditLog.objects.filter(audit_timestamp__gte=date_from)
            if date_to != "":
                logs = AuditLog.objects.filter(audit_timestamp__gte=date_from, audit_timestamp__lte=date_to)
                
        elif date_to != "":
            logs = AuditLog.objects.filter(audit_timestamp__lte=date_to)
            if date_from != "":
                logs = AuditLog.objects.filter(audit_timestamp__gte=date_from, audit_timestamp__lte=date_to)
        
        log = AuditLog.objects.create(audit_name=request.user.username, audit_action="Generated a report on audit trail", audit_module="Reports")
        log.save()    
            
    context = {
        "logs": logs,
    }
    
    return render(request, "reports/audit_report.html", context)