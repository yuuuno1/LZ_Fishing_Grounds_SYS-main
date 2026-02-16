from django.http import JsonResponse
from django.shortcuts import render
from users.models import CustomUser
from PointOfSale.models import *
from Products.models import *
from Order.models import Order
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


now = datetime.date.today()
current_month = now.month
current_year = now.year


@login_required
def index(request):
    page = "dashboard"
    total_users = CustomUser.objects.all().count()
    
    def get_sales_today():
        total = 0
        sales_today_pos = Transaction.objects.filter(date_occured__contains=now)
        sales_today_order = Order.objects.filter(date_occured__contains=now)
        
        for sales in sales_today_pos:
            total += sales.total
            
        for sales2 in sales_today_order:
            total += sales2.total
            
        
        formatted_total = "{:,}".format(total) 
        return formatted_total
    
    def get_sales_current_month():
        
        total = 0
        sales_month_pos = Transaction.objects.filter(date_occured__month=current_month, date_occured__year=current_year)
        sales_month_order = Order.objects.filter(date_occured__month=current_month, date_occured__year=current_year)
        
        for sales in sales_month_pos:
            total += sales.total
            
        for sales2 in sales_month_order:
            total += sales2.total
            
        
        formatted_total = "{:,}".format(total) 
        return formatted_total
    
    
    context = {
        'page_name' : page,
        'total_users' : total_users,
        'get_sales_today': get_sales_today(),
        'get_sales_current_month': get_sales_current_month()
    }
    
    return render(request, 'dashboard/index.html', context)




def chart_data(request):
    
    # get sales by month function
    def get_sales_by_month(month, current_year):
        
        total = 0
        sales_month_pos = Transaction.objects.filter(date_occured__month=month, date_occured__year=current_year)
        sales_month_order = Order.objects.filter(date_occured__month=month, date_occured__year=current_year)
        
        for sales in sales_month_pos:
            total += sales.total
            
        for sales2 in sales_month_order:
            total += sales2.total  
        
        #formatted_total = "{:,}".format(total) 
        return total
    
    
    bar = []
    pie = []
    pie_data = []
    
    # get all sales by month for bar graph
    for i in range(12):
        bar.append(get_sales_by_month(i+1, current_year))
    
    # top 5 items
    items = Item.objects.values('product_id').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:5]
    
    # pie chart data
    for item in items:
        pie.append(item['product_id'])
        pie_data.append(item['total_sales'])

        
    
    return JsonResponse({'bar':bar, 'pie': pie, 'pie_data': pie_data})