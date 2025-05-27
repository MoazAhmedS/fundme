from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create',ReadAndCreateProject.as_view()),
]