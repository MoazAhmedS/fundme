from django.contrib import admin
from django.urls import path, include
from .api.views import RegisterAPIView ,ActivateAccountView
urlpatterns = [
    path('API/register/', RegisterAPIView.as_view()),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view() ,name='activate-account'),

]
