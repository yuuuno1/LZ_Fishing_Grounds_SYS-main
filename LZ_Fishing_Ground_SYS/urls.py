"""
URL configuration for LZ_Fishing_Ground_SYS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import index, tips_guides
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('tips-and-guide/', tips_guides, name='tips_guides'),
    path('users/', include('users.urls')),
    path('dashboard/', include('Dashboard.urls')),
    path('products/', include('Products.urls')),
    path('pos/', include('PointOfSale.urls')),
    path('audit_trail/', include('AuditTrail.urls')),
    path('settings/', include('Settings.urls')),
    path('shop/', include('Shop.urls')),
    path('orders/', include('Order.urls')),
    path('reports/', include('Report.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

