from django.urls import path
from . import views 
from .views import sales_stats

urlpatterns = [
    path('stats/', sales_stats, name='sales_stats'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
