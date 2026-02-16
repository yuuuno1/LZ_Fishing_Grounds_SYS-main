from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path("chart_data/", views.chart_data, name="chart_data")
]
