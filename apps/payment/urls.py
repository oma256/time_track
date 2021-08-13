from django.urls import path

from apps.payment.views import PaymentCreateView, PayboxResultAPIView


app_name = 'payment'

urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='payment_create'),
    path('paybox-result/', PayboxResultAPIView.as_view(), name='paybox-result'),
]
