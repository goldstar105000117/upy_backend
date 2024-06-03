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
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('signout/', views.signout_view, name='signout'),
    path('refresh/', views.refresh_token_view, name='token_refresh'),
    path('confirm_email/', views.confirm_email_view, name='confirm_email'),
    path('confirm_phone/', views.confirm_phone_view, name='confirm_phone'),
    path('resend_email_token/', views.resend_email_token_view, name='resend_email_token'),
    path('resend_phone_code/', views.resend_phone_code_view, name='resend_phone_code'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('reset_password/validate/', views.reset_password_validate_view, name='reset_password_validate'),
    path('reset_password/set/', views.reset_password_validate_view, name='reset_password_set'),
    path('update_password/', views.update_password_view, name='update_password'),
    path('deactivate_account/', views.request_deactivate_account, name='request_deactivate_account'),
    path('deactivate_account/confirm/', views.confirm_deactivate_account, name='confirm_deactivate_account'),
    path('activate_account/', views.request_activate_account, name='request_activate_account'),
    path('activate_account/confirm/', views.confirm_activate_account, name='confirm_activate_account'),
]
