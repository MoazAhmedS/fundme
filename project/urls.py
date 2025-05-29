from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create/',CreateProject.as_view()),
    path('<int:id>/',ProjectDetails.as_view()),
    path('<int:project_id>/comments/', ProjectCommentsView.as_view(), name='project-comments'),

]