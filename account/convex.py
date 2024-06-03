from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.conf import settings
import os
from dotenv import load_dotenv
from convex import ConvexClient

client = ConvexClient(settings.CONVEX_URL)

def update_user(user_data):
    result = client.mutation("user:updateUser", user_data)
    if result['success']:
        return result['result']
    return None

def update_profile(profile_data):
    result = client.mutation("profile:updateProfile", profile_data)
    if result['success']:
        return result['result']
    return None

def insert_interests_tags(interests_tag_data):
    result = client.mutation("intereststags:insertInterestsTags", interests_tag_data)
    if result['success']:
        return result['result']
    return None

def updateInterestsTags(interests_tag_data):
    result = client.mutation("intereststags:updateInterestsTags", interests_tag_data)
    if result['success']:
        return result['result']
    return None

def deleteInterestsTags(interests_tag_data):
    result = client.mutation("intereststags:deleteInterestsTags", interests_tag_data)
    if result['success']:
        return result['result']
    return None

def insertUserInterestsTags(tag_data):
    result = client.mutation("userIntereststags:insertUserInterestsTags", tag_data)
    if result['success']:
        return result['result']
    return None

def getByPhoneNumber(phone_number_data):
    result = client.mutation("profile:getByPhoneNumber", phone_number_data)
    if result['success']:
        return result['result']
    return None

def updateSecurity(security_data):
    result = client.mutation("profile:updateSecurity", security_data)
    if result['success']:
        return result['result']
    return None

def updateNotificationSetting(notification_data):
    result = client.mutation("profile:updateNotificationSetting", notification_data)
    if result['success']:
        return result['result']
    return None

def updateEnableNotification(enable_notification_data):
    result = client.mutation("profile:updateEnableNotification", enable_notification_data)
    if result['success']:
        return result['result']
    return None

def generateConfirmToken(tokens_data):
    result = client.mutation("tokens:generateConfirmToken", tokens_data)
    if result['success']:
        return result['result']
    return None

def getByTokenAndTypeAndUserId(tokens_data):
    result = client.mutation("tokens:getByTokenAndTypeAndUserId", tokens_data)
    if result['success']:
        return result['result']
    return None

def deleteTokenById(tokens_data):
    result = client.mutation("tokens:deleteTokenById", tokens_data)
    if result['success']:
        return result['result']
    return None

def updateUserEmail(user_data):
    result = client.mutation("user:updateUserEmail", user_data)
    if result['success']:
        return result['result']
    return None

def insertNewEmail(new_email_data):
    result = client.mutation("usernewemails:insertNewEmail", new_email_data)
    if result['success']:
        return result['result']
    return None

def getNewEmailsByUserId(new_email_data):
    result = client.mutation("usernewemails:getByUserId", new_email_data)
    if result['success']:
        return result['result']
    return None