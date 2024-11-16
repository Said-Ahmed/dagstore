from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartApiViewSet.as_view({'get': 'list'}), name='cart_list'),

    path('add/<uuid:product_uuid>/', views.CartApiViewSet.as_view({'post': 'create'}), name='cart_add'),

    path('remove/<uuid:product_uuid>/', views.CartApiViewSet.as_view({'delete': 'destroy'}), name='cart_remove'),

    path('clear/', views.CartApiViewSet.as_view({'delete': 'clear_cart'}), name='cart_clear'),
]