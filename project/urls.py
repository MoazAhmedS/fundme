from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create/',CreateProject.as_view()),
    path('<int:id>/',ReadUpdateDeleteProjectByID.as_view()),
    path('<int:project_id>/comments/', ProjectCommentsView.as_view(), name='project-comments'),
    path('cancel/<int:project_id>/', CancelProjectAPIView.as_view(), name='cancel_project'),

]