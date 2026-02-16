from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="shop"),
    path("view-all/", views.all_product, name="all_product"),
    path("item/<int:id>/", views.view_product, name="view_item"),
    path("item/<int:id>/delete/", views.delete_cart_item, name="del_cart_item"),
    path("my-cart/", views.cart_view, name="cart_view"),
    path("checkout/", views.checkout_view, name="checkout_view"),
    path("orders/", views.orders_view, name="orders_view"),
    path("orders/<int:id>/", views.view_order, name="view_order"),
    path("receipt/<int:order_id>/", views.receipt_printable, name="print_order_receipt"),
    
]
