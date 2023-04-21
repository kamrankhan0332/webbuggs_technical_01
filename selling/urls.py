from django.urls import path
from .views import *


urlpatterns = [
    path('colors/', color_list, name='color_list'),
    path('colors/<int:pk>/', color_detail, name='color_detail'),
    path('sub/', subcategory_list, name='sub_category_list'),
    path('sub/<int:pk>/', subcategory_detail, name='sub_category_detail'),
    path('product/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('top_three_categories/', top_three_categories, name='top_three_categories'),
    path('product_filter/', product_filter, name='product_filter'),
]
