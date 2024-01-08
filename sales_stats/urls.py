from django.urls import path
from .views import sales_stats

urlpatterns = [
    path('stats/', sales_stats, name='sales_stats'),
]
