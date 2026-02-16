from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="reports"),
    path("users/", views.user_report, name="user_reports"),
    path("products/", views.product_report, name="product_reports"),
    path("stockslog/", views.stockslog_report, name="stockslog_report"),
    path("pos/", views.pos_report, name="pos_report"),
    path("shop/", views.shop_report, name="pos_report"),
    path("audit/", views.audit_report, name="audit_report"),
]
