from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.get_plans_view, name='get_plans'),
]
