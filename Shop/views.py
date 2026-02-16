from django.shortcuts import redirect, render
from Products.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from Order.forms import *
from Order.models import *
from PointOfSale.models import Item as Item2
import datetime

@login_required
def index(request):
    top_fish = []
    featured = FeaturedProduct.objects.select_related('product')
    products = Products.objects.all()[:8]
    
    items = Item2.objects.values('product_id').annotate(total_sales=Sum('quantity')).order_by('-total_sales')
    
    for item in items:
        #print(item['product_id'])
        fishes = Products.objects.filter(name=item['product_id']).filter(category__category__icontains="fish")
        
        for product in fishes:
            if len(top_fish) < 6:
                top_fish.append(product)

        
    context = {
        'featured': featured,
        'products': products,
        'top_fish': top_fish 
    }
    
    return render(request, "shop/index.html", context)


@login_required
def all_product(request):
    
    products = Products.objects.filter(stocks__gt=0).filter(is_available=True)
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        products = Products.objects.filter(stocks__gt=0).filter(is_available=True).filter(name__icontains=search)
        
    if request.GET.get('filter'):
        filter = request.GET.get('filter')
        products = Products.objects.filter(stocks__gt=0).filter(is_available=True).filter(category__category__icontains=filter)
        
    
        
        
    categories = Product_Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    
    return render(request, "shop/AllProduct.html", context)


@login_required
def view_product(request, id):
    
    product = Products.objects.get(id=id)
    
    if request.method == "POST":
        item_quantity = request.POST.get('add_to_cart')
        cart = Cart.objects.get(customer=request.user)
        quantity = int(item_quantity)
        item = Item.objects.filter(cart=cart).filter(product=product)

        # check whether the item is already in the cart
        if not item.exists():
            # ONLY FOR ITEMS THAT ARE NOT YET IN THE CART
            if quantity <= product.stocks and quantity > 0: 
                add_item = Item(cart=cart, product=product, quantity=quantity)  
                add_item.save()
                messages.add_message(request, messages.SUCCESS, f"Item has been added to the cart.") 
            else:
                messages.add_message(request, messages.ERROR, f"Failed to add to cart.")
        
        else:
            
            # ONLY FOR ITEMS THAT ALREADY IN THE CART
            for i in item:
                # checks if the quantity + the current quantity in the cart will exceed the current stocks
                if product.stocks < quantity + i.quantity:
                    messages.add_message(request, messages.ERROR, f"Desired quantity exceeds the current stocks.")
                else:
                    i.quantity += quantity
                    i.save()
                    messages.add_message(request, messages.SUCCESS, f"Cart has been updated.")
            
        
    context = {
        'product': product,
    }
    
    
    
    return render(request, "shop/ViewItem.html", context)



@login_required
def cart_view(request):
    
    cart = Cart.objects.get(customer=request.user)
    items = Item.objects.filter(cart=cart)
    current_total = 0
    
    for item in items:
        current_total = item.price() + current_total  
    
    subtotal = "{:,}".format(current_total)
    
    context = {
        'items': items,
        'subtotal': subtotal
    }
    
    return render(request, "shop/cart.html", context)


@login_required
def delete_cart_item(request, id):
    
    item = Item.objects.get(id=id)
    
    item.delete()
    
    
    return redirect('cart_view')



@login_required
def checkout_view(request):
    shop_details = ShopDetails.objects.get(id=1)
    customer = request.user
    form = OrderForm()
    cart = Cart.objects.get(customer=request.user)
    items = Item.objects.filter(cart=cart)
    current_total = 0
    
    for item in items:
        current_total = item.price() + current_total  
    
    subtotal = "{:,}".format(current_total)
    
    current_datetime = datetime.datetime.now()
    order_id = current_datetime.strftime("%Y%m%d%H%M%S")
        
    cart = Cart.objects.get(customer=request.user)
    
    if request.method == 'POST':
        
        form = OrderForm(request.POST, request.FILES or None)
        
        form.total = current_total
        
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.id = order_id
            order.total = current_total
            
            order.save()
            
            cartitems = Item.objects.filter(cart=cart)
            
            current_order = Order.objects.get(id=order_id)
            
            for item in cartitems:
                product = Products.objects.get(id=item.product.id)
                order_item = OrderItem(order=current_order, product=product, quantity=item.quantity)
                order_item.save()
                
                item.delete()
                
                
            messages.add_message(request, messages.SUCCESS, f"Order has been placed.")
            
            return redirect('orders_view')
        
        else:
            
            messages.add_message(request, messages.ERROR, f"Failed to process order.")
            
    context = {
        'items': items,
        'subtotal': subtotal,
        'form': form,
        'raw_total': current_total,
        'shop_details': shop_details
    }
    
    return render(request, "shop/checkout.html", context)

@login_required
def orders_view(request):
    
    orders = Order.objects.filter(customer=request.user).order_by('-id')
    
    context = {
        'orders': orders,
    }
    
    return render(request, "shop/orders.html", context)

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
    
    return render(request, "shop/view_order.html", context)



def receipt_printable(request, order_id):
    order = Order.objects.get(id=order_id)
    
    shop_details = ShopDetails.objects.get(id=1)
    
    items = OrderItem.objects.filter(order=order)
    
    current_total = 0
    
    for item in items:
        current_total = item.price() + current_total  
    
    subtotal = "{:,}".format(current_total)
    
    context = {
        'subtotal': subtotal,
        'items': items,
        'tnum': order_id,
        'details': shop_details,
        'order': order
    }
    
    return render(request, "shop/receipt_printable.html", context)