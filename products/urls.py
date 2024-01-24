from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),  # noqa
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),  # noqa
    path('remove_from_favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),  # noqa
    path('favorites/', views.user_favorites, name='user_favorites'),
]
