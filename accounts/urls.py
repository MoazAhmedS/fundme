from django.contrib import admin
from django.urls import path, include
from .api.views import RegisterAPIView ,ActivateAccountView,LoginAPIView, FacebookLogin, ForgotPasswordAPIView
urlpatterns = [
    path('API/register/', RegisterAPIView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view() ,name='activate-account'),
    path('API/Login/', LoginAPIView.as_view() ), 
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', ForgotPasswordAPIView.as_view(), name='reset-password'),
]
