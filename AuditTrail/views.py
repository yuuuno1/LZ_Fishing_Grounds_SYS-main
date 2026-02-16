from django.shortcuts import render
from django.core.paginator import Paginator
from .models import AuditLog
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def index(request):
    
    auditlog = AuditLog.objects.all().order_by('-id')
    search = ""
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        request.session['search'] = search
        
        auditlog = AuditLog.objects.filter(Q(audit_action__icontains=search) | Q(audit_name__icontains=search) | Q(audit_module__icontains=search))
           
    page = "audit"
    
    # pagination
    paginator = Paginator(auditlog, 5) # shows 4 logs per page
    
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    # variables rendered to the template
    context = {
        'page_name': page,
        'auditlog': auditlog,
        'page_obj': page_obj,
        'page_char' : 'a' * page_obj.paginator.num_pages,
        'search': search
    }

    return render(request, "audit/index.html", context)