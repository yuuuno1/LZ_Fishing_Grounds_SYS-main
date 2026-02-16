from django.shortcuts import get_object_or_404, redirect, render
from AuditTrail.models import AuditLog
from .forms import *
from .models import Products, StocksLog
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required


# Main Page of Products in admin side
@login_required
def index(request):
    
    products = Products.objects.all().order_by('-id')
    
    if request.GET.get("search"):
        if request.GET.get("search") is not None:
          
            search = request.GET.get("search")
            products = Products.objects.filter(Q(name__icontains=search) | Q(sub_category__icontains=search)).order_by('-id')
    page = "products"
    
    # pagination
    paginator = Paginator(products, 5) # shows 4 users per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'products': products,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages,
        
    }
    
    return render(request, "products/index.html", context)

# add product page
@login_required
def create_product_page(request):
    
    form = ProductCreationForm()
    
    if request.method == "POST":
        form = ProductCreationForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            current_datetime = datetime.datetime.now()
            prod_id = current_datetime.strftime("%Y%m%d%H%M%S")
            
            product = form.save(commit=False)
            
            product.id = prod_id
            product.save()
            
            messages.add_message(request, messages.SUCCESS, "New product has been registered successfully.")
            
            audit = AuditLog(audit_name=request.user.username, audit_action="Registered a product.", audit_module="Product Managements")
            audit.save()
            return redirect('product_management')
        
        else:
            messages.add_message(request, messages.ERROR, "An error occured during the transaction.")
        
    context = {
        'form': form
    }
    return render(request, "products/new_product.html", context)

# update product page
@login_required
def update_product_page(request, id):
    
    obj = get_object_or_404(Products, id=id)
    
    form = ProductChangeForm(request.POST or None, request.FILES or None, instance = obj)
    
    
    if request.method == "POST":
        
        if form.is_valid():
            
            form.save()
            messages.add_message(request, messages.SUCCESS, f"{obj.name} has been successfully updated.")
            audit = AuditLog(audit_name=request.user.username, audit_action="Updated a product.", audit_module="Product Managements")
            audit.save()
            return redirect('product_management')
        
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, "An error occured while updating procudt.")
            
    context = {
        'form': form
    }
    
    
    return render(request, "products/update_product.html", context)

@login_required
def stocks_view(request):
    
    products = Products.objects.all().order_by('-id')
    
    if request.GET.get("search"):
        if request.GET.get("search") is not None:
          
            search = request.GET.get("search")
            products = Products.objects.filter(Q(name__icontains=search) | Q(category__category__icontains=search) | Q(sub_category__icontains=search)).order_by('-id')
            
    page = "stocks"
    
    # pagination
    paginator = Paginator(products, 5) # shows 4 users per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'products': products,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages
    }
    
    return render(request, "products/stocks_management.html", context)


# add stocks page
@login_required
def add_stocks_view(request, id):
    
    obj = get_object_or_404(Products, id=id)
    
    form = AddStockForm()
    
    if request.method == "POST":
        form = AddStockForm(request.POST)
        if form.is_valid():
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
            
            product_name = obj.name
           # current_stocks = obj.stocks
            stocks_added = form.cleaned_data['stocks_added']
            supplier = form.cleaned_data['supplier']
            total_cost = form.cleaned_data['total_cost']
            
            added_by = request.user.username
            
            new_stocks = StocksLog.objects.create(id=formatted_datetime, product_id=obj, stocks_added=stocks_added, supplier=supplier, total_cost=total_cost, added_by=added_by)
            
            
            new_stocks.save()
            obj.stocks += stocks_added
            obj.save()
            
            audit = AuditLog(audit_name=request.user.username, audit_action=f"Added a stock on product id {id}.", audit_module="Stocks Managements")
            audit.save()
            
            messages.add_message(request, messages.SUCCESS, f"{obj.name}'s stocks has been updated successfully.")
            return redirect('stocks_management')
        
        else:
            messages.add_message(request, messages.ERROR, "An error occured while processing the transaction.")
            
    context = {
        'form': form,
        'product': obj
    }
    
    
    return render(request, "products/add_stocks.html", context)


# dispose stocks page
@login_required
def dispose_stocks(request, id):
    
    product = Products.objects.get(id=id)
    
    form = DisposeStockForm()
    
    if request.method == "POST":
        form = DisposeStockForm(request.POST)
        
        if form.is_valid():
            dispose = int(form.cleaned_data['stocks_to_dispose'])
            reason = form.cleaned_data['reason']
            
            if dispose < product.stocks:
                product.stocks -= dispose
                product.save()
                
                dispose_log = DisposeLog(product=product, dispose=dispose, reason=reason, disposed_by=request.user)
                dispose_log.save()
                
                audit = AuditLog(audit_name=request.user.username, audit_action=f"Disposed a stock on product id {id}.", audit_module="Stocks Management")
                audit.save()
                
                messages.add_message(request, messages.SUCCESS, f"Disposed a stock on product {product.name}.")
                return redirect('stocks_management')
            
                
            else:
                messages.add_message(request, messages.ERROR, "Dispose stocks cannot be greater than the current stocks.")  
        
        else:
            messages.add_message(request, messages.ERROR, "All fields are required")
            
    context = {
        'form': form,
        'product': product
    }
    
    
    return render(request, "products/dispose_stock.html", context)


@login_required
def stockslog_view(request):
    stockslog = StocksLog.objects.all().order_by('-id')
    
    page = "stocks"
    
    # pagination
    paginator = Paginator(stockslog, 5) # shows 4 logs per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'stockslog': stockslog,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages
    }
    
    return render(request, "products/stocks_logs.html", context)

@login_required
def disposed_view(request):
    disposed_logs = DisposeLog.objects.all().order_by('-id')
    
    page = "stocks"
    
    # pagination
    paginator = Paginator(disposed_logs, 5) # shows 4 logs per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'stockslog': disposed_logs,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages
    }
    
    return render(request, "products/disposed_logs.html", context)