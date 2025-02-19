from django.urls import path
from . import views

app_name = 'store'


urlpatterns = [
    path('products/', views.ProductApiViewSet.as_view({'get': 'list'}), name='product_list'),

    path('products/<uuid:uuid>/<slug:slug>/', views.ProductApiViewSet.as_view({'get': 'retrieve'}), name='product_detail'),

    path('products/<slug:category_slug>/', views.ProductApiViewSet.as_view({'get': 'list'}), name='product_list_by_category'),

    path('category/', views.CategoryView.as_view({'get': 'list'}), name='category_list')
]