from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.get_plans_view, name='get_plans'),
    path('plans/create/', views.create_plan_view, name='create_plan'),
    path('plans/<str:pk>/', views.update_plan_view, name='update_plan'),
]
