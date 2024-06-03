from django.urls import path
from . import views

urlpatterns = [
    path('airlines/', views.get_airlines_view, name='get_airlines'),
]
