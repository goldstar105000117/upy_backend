from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.get_plans_view, name='get_plans'),
    path('plans/create/', views.create_plan_view, name='create_plan'),
    path('plans/<str:pk>/', views.update_plan_view, name='update_plan'),
    path('plans/<str:pk>/activate/', views.activate_plan_view, name='activate_plan'),
    path('plans/<str:pk>/deactivate/', views.deactivate_plan_view, name='deactivate_plan'),
    path('payment_intent/create/', views.create_stripe_payment_intent_view, name='create_stripe_payment_intent'),
    path('payment_intent/confirm/', views.confirm_stripe_payment_intent_view, name='confirm_stripe_payment_intent'),
    path('<str:pk>/cancel/', views.cancel_subscription_view, name='cancel_subscription'),
    path('<str:pk>/update/', views.upgrade_subscription_view, name='upgrade_subscription'),
    path('stripe/incoming/', views.stripe_incoming_view, name='stripe_incoming'),
]
