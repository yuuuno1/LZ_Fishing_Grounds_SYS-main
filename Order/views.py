from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.



@login_required
def index(request):

    orders = Order.objects.all().order_by('-id')
    
    if request.GET.get("search"):
        if request.GET.get("search") is not None:
          
            search = request.GET.get("search")
            orders = Order.objects.filter(id__icontains=search).order_by('-id')
            
    page_name = "eorders"
    
    # pagination
    paginator = Paginator(orders, 5) # shows 5 per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    context = {
        'orders': orders,
        'page_name': page_name,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages
    }
    
    return render(request, "orders/index.html", context)


@login_required
def view_order(request, id):
    
    order = Order.objects.get(id=id)
    items = OrderItem.objects.filter(order=order)
    
    current_total = 0
    
    for item in items:
        current_total = item.price() + current_total  
    
    subtotal = "{:,}".format(current_total)
    
    context = {
        'items': items,
        'subtotal': subtotal,
        'id': id
    }
    
    return render(request, "orders/view_order.html", context)


@login_required
def verify_order(request, id):
    
    order = Order.objects.get(id=id)
    items = OrderItem.objects.filter(order=order)
    
    current_total = 0
    
    for item in items:
        current_total = item.price() + current_total  
    
    subtotal = "{:,}".format(current_total)
    
    context = {
        'items': items,
        'subtotal': subtotal,
        'id': id
    }
    
    return render(request, "orders/verify_order.html", context)


def verify(request, id):
    
    order = Order.objects.get(id=id)
    # items = OrderItem.objects.filter(order=order)
    order.status = 'preparing'
    order.save()
    
    messages.add_message(request, messages.SUCCESS, f"Order {id} has been verified and now preparing.")
    
    # send email
    send_mail(
        "Order is being processed - LZ Fishing Grounds",
        "Please do not reply to this email, this email is auto generated.",
        "LZ.Fishing.Grounds@gmail.com",
        [str(order.customer.email)],
        fail_silently=False,
        html_message=f"<h3 style='margin:20px 0;'> Your order with Order ID: {order.id} is now currently being prepared please check our site for monitoring, Thank you and have a great day! </h3>",
    )
    
    return redirect('e_orders')
        
        
        
def for_pickup(request, id):
    
    order = Order.objects.get(id=id)
    # items = OrderItem.objects.filter(order=order)
    # order.status = 'preparing'
    # order.save()
    items = OrderItem.objects.filter(order=order)
    errors = []
    
    # check if stocks is sufficient for all items
    for item in items:
        product = Products.objects.get(id=item.product.id)
        
        if product.stocks < item.quantity:
            errors.append(f"Error on product {item.product.name} the stock is insufficient.")

    
    if len(errors) > 0:
        print(errors)
        messages.add_message(request, messages.ERROR, f"Order {id} has some conflicts regarding the available stocks and the ordered stocks.")
        
    else:
        
        for item in items:
            product = Products.objects.get(id=item.product.id)
            product.stocks -= item.quantity
            product.save()
        
        order.status = "ready"
        
        order.save()
        
        messages.add_message(request, messages.SUCCESS, f"Order {id} has been set for pickup.")
        
        # send email
        send_mail(
            "Order is now ready for pickup - LZ Fishing Grounds",
            "Please do not reply to this email, this email is auto generated.",
            "LZ.Fishing.Grounds@gmail.com",
            [str(order.customer.email)],
            fail_silently=False,
            html_message=f"<h3 style='margin:20px 0;'> Your order with Order ID: {order.id} is now ready for pickup, please go to our store, Thank you for using our site and have a great day! </h3>",
        )
    
    return redirect('e_orders')
    
    
    
def complete_order(request, id):
    order = Order.objects.get(id=id)
    
    order.status = "complete"
    order.save()
    
    messages.add_message(request, messages.SUCCESS, f"Order {id} has been picked up.")
    
    # send email
    send_mail(
            "Order is now complete - LZ Fishing Grounds",
            "Please do not reply to this email, this email is auto generated.",
            "LZ.Fishing.Grounds@gmail.com",
            [str(order.customer.email)],
            fail_silently=False,
            html_message=f"<h3 style='margin:20px 0;'> Your order with Order ID: {order.id} is now complete, Thank you for shopping with us and for using our site, have a great day! </h3>",
    )
    
    return redirect('e_orders')
    

def cancel_order(request, id):
    
    order = Order.objects.get(id=id)
    
    order.status = "cancelled"
    order.save()
    
    messages.add_message(request, messages.ERROR, f"Order {id} has been cancelled.")
    
    # send email
    send_mail(
            "Order has been cancelled - LZ Fishing Grounds",
            "Please do not reply to this email, this email is auto generated.",
            "LZ.Fishing.Grounds@gmail.com",
            [str(order.customer.email)],
            fail_silently=False,
            html_message=f"<h3 style='margin:20px 0;'> Your order with Order ID: {order.id} has been cancelled due to some issues, if you have paid for any amount through gcash please go to our store to get the refund. For more clarification please talk to any of our staff in the store and provide the order ID and any proof of payment. Thank you and have a great day.</h3>",
    )
    
    return redirect('e_orders')