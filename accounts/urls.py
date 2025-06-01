from django.contrib import admin
from django.urls import path, include
from .api.views import *
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view() ,name='activate-account'),
    path('Login/', LoginAPIView.as_view() ), 
    path('auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', UserProfileUpdateAPIView.as_view(), name='user-profile-edit'),
    path('profile/delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('logout/', LogoutAPIView.as_view(), name='logout-account'),
]