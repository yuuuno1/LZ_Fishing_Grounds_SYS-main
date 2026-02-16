import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from AuditTrail.models import AuditLog
from Products.models import Products
from django.contrib import messages
from . models import Cart, Item, Transaction
from django.db.models import Sum, Q
import locale
from decimal import Decimal
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.decorators import login_required
from Shop.models import ShopDetails


# Create your views here.
@login_required
def index(request):
    
    page_name = "pos"
    products = Products.objects.all()
    
    if request.GET.get("search"):
        search = request.GET.get("search")
        products = Products.objects.filter(Q(name__icontains=search) | Q(category__category__icontains=search))

        if products.first() is None:
            products = Products.objects.all().order_by('-id')
    
    cart = Cart.objects.all().order_by('-id')
    cart_size = len(cart)
    
    # adding items to cart
    if request.method == "POST":
        prod_id = request.POST.get("id")
        quantity = request.POST.get("quantity")
        quantity = int(quantity)
        
        if prod_id and quantity > 0:
            product = Products.objects.get(id=int(prod_id))
            
            _cart = Cart.objects.filter(product_id = prod_id).first()
            
            # checks if the item is alreaddy at the cart if yes, update the item info but if not just create it
            if _cart is None:
                if product.stocks >= quantity:
                    subtotal_item = product.price * quantity
                    
                    new_cart = Cart(product_id=product, product_name=product.name, quantity=quantity, subtotal=subtotal_item)
                    new_cart.save()
                    
                    audit = AuditLog(audit_name=request.user.username, audit_action="Added item to the cart.", audit_module="Point of Sale")
                    audit.save()
                    
                    return JsonResponse({"success": True})
                else:
                    messages.add_message(request, messages.ERROR, "Desired quantity exceeded current stocks.")
                    return JsonResponse({"err": "Desired quantity exceeded current stocks", "success": False})
            else:
                if product.stocks >= _cart.quantity + quantity:
                    _cart.quantity += quantity
                    _cart.subtotal += product.price * quantity
                    _cart.save()
                    return JsonResponse({"success": True})
                else:
                    messages.add_message(request, messages.ERROR, "Desired quantity exceeded current stocks.")
                    return JsonResponse({"err": "Desired quantity exceeded current stocks", "success": False})
        
        else:
            messages.add_message(request, messages.ERROR, "Invalid Request.")
            print("Invalid Request")
        
    
    cart_subtotal = Cart.objects.aggregate(Sum('subtotal'))
        
    if cart_subtotal['subtotal__sum'] is not None:
        
        cart_subtotal = "{:,}".format(cart_subtotal['subtotal__sum'])
        # cart_subtotal = cart_subtotal['subtotal__sum']
    else:
        cart_subtotal = "0.00"
    context = {
        'page_name': page_name,
        'products': products,
        'cart': cart,
        'cart_size': cart_size,
        'cart_subtotal': cart_subtotal,
    }
    
 
    return render(request, "./pos/index.html", context)


@login_required
def delete_item(request, id):
    
    item = Cart.objects.get(pk=id)
        
    if item is None:
         messages.add_message(request, messages.ERROR, "Item was not member of the cart.")
    else:
        item.delete()
        audit = AuditLog(audit_name=request.user.username, audit_action="Deleted item from cart.", audit_module="Point of Sale")
        audit.save()
        
    return redirect("pos")


@login_required
def transaction_view(request):
    cart = Cart.objects.all()
    
    if request.method == "POST":
    
                 current_datetime = datetime.datetime.now()
                 transaction_id = current_datetime.strftime("%Y%m%d%H%M%S")
                 cart_subtotal = Cart.objects.aggregate(Sum('subtotal'))['subtotal__sum']
            # change = 0
            # payment = Decimal(request.POST.get('payment'))
            # payment_type = request.POST.get('payment_type')
            
            #if payment >= cart_subtotal:
                #  change = payment - cart_subtotal
                 new_transaction = Transaction(id=transaction_id, cashier=request.user.username, total=cart_subtotal)
                 
                 new_transaction.save()
                 
                 transaction = Transaction.objects.all().order_by('-id').first()
                 
                 for item in cart:
                     new_item = Item(tnum=transaction, quantity=item.quantity, subtotal=item.subtotal, product_id=item.product_id)
                     new_item.save()
                     
                    #  prod = Products.objects.get(id=item.product_id.id)
                    #  prod.stocks -= item.quantity
                    #  prod.save()
                     
                     item.delete()
                     
                 messages.add_message(request, messages.SUCCESS, "Transaction has been placed for confirmation")
                 return redirect('pos')
            # else:
            #     messages.add_message(request, messages.ERROR, "Insufficient amount")
            #     return redirect('pos')
    
@login_required            
def trasactions(request):
        
    trasactions = Transaction.objects.all().order_by('-id')
    
    if request.GET.get("search"):
        if request.GET.get("search") is not None:
          
            search = request.GET.get("search")
            trasactions = Transaction.objects.filter(Q(id__icontains=search) | Q(status__icontains=search) | Q(payment_method__icontains=search)).order_by('-id')
            
            audit = AuditLog(audit_name=request.user.username, audit_action="Searched from Transactions.", audit_module="Point of Sale")
            audit.save()
            
    page = "orders"
    
    # pagination
    paginator = Paginator(trasactions, 5) # shows 4 users per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages
    }
    
    return render(request, "pos/transactions.html", context)

@login_required
def cancel_transaction(request):
    Cart.objects.all().delete()
    messages.add_message(request, messages.SUCCESS, "Transaction has been cleared.")
    
    audit = AuditLog(audit_name=request.user.username, audit_action="Cancelled a transacction.", audit_module="Point of Sale")
    audit.save()
    return redirect('pos')

@login_required
def payment_view(request, id):

    page_name = "pos"
    
    items = Item.objects.filter(tnum=id).order_by('-id')
    subtotal_raw = Item.objects.filter(tnum=id).aggregate(Sum('subtotal'))
        
    if subtotal_raw['subtotal__sum'] is not None:
        
        subtotal = "{:,.2f}".format(subtotal_raw['subtotal__sum'])
        
        
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        tnum = request.POST.get("tnum")
        if payment_method is not None and payment_method == "cash":
            # print("cash")
            if request.POST.get("payment") is not None and int(request.POST.get("payment")) >= subtotal_raw['subtotal__sum']:
                payment = int(request.POST.get("payment"))
                change = payment - subtotal_raw['subtotal__sum']
                
                method = "cash"
                status = "complete"
                
                transaction = Transaction.objects.get(id=int(tnum))
                err = 0
                
                for item in items:
                    product = Products.objects.get(name=item.product_id)
                    if product.stocks >= item.quantity:
                        product.stocks -= item.quantity
                        product.save()
                    else:
                        err += 1
                    
                    
                if err == 0:
                    transaction.payment = payment
                    transaction.change = change
                    transaction.status = status
                    transaction.payment_method = method
                    transaction.date_occured = datetime.datetime.now()
                    transaction.save()
                
                    messages.add_message(request, messages.SUCCESS, "Transaction has been compeleted.")
                    
                    audit = AuditLog(audit_name=request.user.username, audit_action="Completed a cash transaction.", audit_module="Point of Sale")
                    audit.save()
                
                    return redirect("transaction_views")
                
                else:
                    messages.add_message(request, messages.ERROR, "Transaction has been cancelled due to an item stock being insufficient.")
                    return redirect("transaction_views")
                    
                
        elif payment_method is not None and payment_method == "gcash":
                tnum = request.POST.get("tnum")
                payment = subtotal_raw['subtotal__sum']
                change = 0
                
                method = "gcash"
                status = "complete"
                ref = request.POST.get("ref")
                gcash = request.POST.get("num")
                
                transaction = Transaction.objects.get(id=int(tnum))
                err = 0
                
                for item in items:
                    product = Products.objects.get(name=item.product_id)
                    if product.stocks >= item.quantity:
                        product.stocks -= item.quantity
                        product.save()
                    else:
                        err += 1
                    
                    
                if err == 0:
                    transaction.payment = payment
                    transaction.change = change
                    transaction.status = status
                    transaction.gcash_num = gcash
                    transaction.ref = ref
                    transaction.payment_method = method
                    transaction.date_occured = datetime.datetime.now()
                    transaction.save()
                
                    messages.add_message(request, messages.SUCCESS, "Transaction has been compeleted.")

                    
                    audit = AuditLog(audit_name=request.user.username, audit_action="Completed a gcash transaction.", audit_module="Point of Sale")
                    audit.save()
                    
                    
                    return redirect("transaction_views")
                
                else:
                    messages.add_message(request, messages.ERROR, "Transaction has been cancelled due to an item stock being insufficient.")
                    return redirect("transaction_views")
            
            
        
    context = {
        'page_name': page_name,
        'tnum': id,
        'items': items,
        'subtotal': subtotal,
        'subtotal_raw': subtotal_raw['subtotal__sum'],
    }
 

    return render(request, "pos/payment.html", context)
    
    
@login_required 
def cancel_payment_view(request, id):

    page_name = "pos"
            
      
    if request.GET.get('confirm') is not None:
        
        if request.GET.get('confirm') == "yes":
            
            transaction = Transaction.objects.get(id=int(id))
            transaction.status = "cancelled"
            transaction.save()
            
            messages.add_message(request, messages.SUCCESS, "Transaction has been voided.")
            
            audit = AuditLog(audit_name=request.user.username, audit_action="Cancelled pending transaction.", audit_module="Point of Sale")
            audit.save()
            
            return redirect("transaction_views")
            
    context = {
        'page_name': page_name,
        'tnum': id,

    }
 

    return render(request, "pos/cancel_payment.html", context)


@login_required
def receipt(request, id):
    page_name = "pos"
    
    order = Transaction.objects.get(id=id)
    
    items = Item.objects.filter(tnum__id=id).order_by('-id')
    
    subtotal_raw = Item.objects.filter(tnum__id=id).aggregate(Sum('subtotal'))

    if subtotal_raw['subtotal__sum'] is not None:

        subtotal = "{:,.2f}".format(subtotal_raw['subtotal__sum'])
    
    context = {
        'order': order,
        'page_name': page_name,
        'subtotal': subtotal,
        'items': items,
        'subtotal_raw': subtotal_raw,
        'tnum': id,
    }
    
    return render(request, "pos/receipt.html", context)



def receipt_printable(request, order_id):
    order = Transaction.objects.get(id=order_id)
    
    shop_details = ShopDetails.objects.get(id=1)
    items = Item.objects.filter(tnum=order_id)
    
    subtotal_raw = Item.objects.filter(tnum__id=order_id).aggregate(Sum('subtotal'))
    
    if subtotal_raw['subtotal__sum'] is not None:

        subtotal = "{:,.2f}".format(subtotal_raw['subtotal__sum'])
    
    context = {
        'subtotal': subtotal,
        'items': items,
        'subtotal_raw': subtotal_raw,
        'tnum': order_id,
        'details': shop_details,
        'order': order
    }
    
    return render(request, "pos/receipt_printable.html", context)