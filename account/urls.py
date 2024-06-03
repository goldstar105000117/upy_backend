"""
URL configuration for updatedai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user/profile/update/', views.update_profile_data, name='update_profile_data'),
    path('interests_tags/create/', views.create_interests_tag, name='create_interests_tag'),
    path('interests_tags/<str:pk>/', views.update_interests_tag, name='update_interests_tag'),
    path('user/profile/interests_tags/', views.insert_interests_tag_user, name='insert_interests_tag_user'),
    path('user/profile/security/', views.update_security, name='update_security'),
    path('user/profile/notification_setting/', views.update_email_notification_settings, name='update_email_notification_settings'),
    path('user/profile/enable_notification/', views.enable_notification, name='enable_notification'),
    path('user/profile/disable_notification/', views.disable_notification, name='disable_notification'),
    path('user/profile/update_email/', views.request_update_email, name='request_update_email'),
    path('user/profile/update_email/original/confirm/', views.confirm_update_original_email, name='confirm_update_original_email'),
    path('user/profile/update_email/new/confirm/', views.confirm_update_new_email, name='confirm_update_new_email'),
]
