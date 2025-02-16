from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('process/', views.PaymentApiView.as_view({'post': 'create'}), name='payment_create'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
]