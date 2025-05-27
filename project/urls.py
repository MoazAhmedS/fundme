from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create',CreateProject.as_view()),
    path('<int:id>/',ReadUpdateDeleteProjectByID.as_view()),
]