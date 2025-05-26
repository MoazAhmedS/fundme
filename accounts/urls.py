from django.contrib import admin
from django.urls import path, include
from .api.views import RegisterAPIView 
urlpatterns = [
    path('API/register/', RegisterAPIView.as_view()),
]
