from django.urls import path
from . import views

urlpatterns = [
    path('payment_intent/create/', views.create_stripe_payment_intent_view, name='create_stripe_payment_intent'),
    path('payment_intent/confirm/', views.confirm_stripe_payment_intent_view, name='confirm_stripe_payment_intent'),
]
