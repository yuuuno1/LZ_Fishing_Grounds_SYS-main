from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="e_orders"),
    path("view_order/<int:id>/", views.view_order, name="view_order_inside"),
    path("verify_order/<int:id>/", views.verify_order, name="verify_order"),
    path("verify/<int:id>/", views.verify, name="_verify"),
    path("setPickup/<int:id>/", views.for_pickup, name="_pickup"),
    path("complete/<int:id>/", views.complete_order, name="completed"),
    path("cancel/<int:id>/", views.cancel_order, name="cancel_order"),
]
