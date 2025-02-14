from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderApiView.as_view({'get': 'list'}), name='order_create'),
]