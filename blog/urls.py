from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('add/', views.add_post, name='add_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('add_to_favorite_posts/<int:pk>/', views.add_to_favorite_posts, name='add_to_favorite_posts'),  # noqa
    path('favorite_posts/', views.favorite_posts_list, name='favorite_posts_list'),  # noqa
    path('remove_from_favorite_posts/<int:pk>/', views.remove_from_favorite_posts, name='remove_from_favorite_posts'),  # noqa
]
