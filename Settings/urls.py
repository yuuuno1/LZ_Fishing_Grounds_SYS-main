from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="settings"),
    path("add_product_category/", views.add_product_category, name="add_prod_cat"),
    path("add_supplier/", views.add_supplier, name="add_supplier"),
]
