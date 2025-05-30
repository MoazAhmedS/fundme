from django.urls import path
from project.api.views import *
urlpatterns = [
    path('Create/',CreateProject.as_view()),
    path('<int:id>/',ProjectDetails.as_view()),
    path('<int:project_id>/comments/', ProjectCommentsView.as_view(), name='project-comments'),
    path('api/createCategory/', CreateCategoryView.as_view(), name='create-category'),
    path('cancel/<int:project_id>/', CancelProjectAPIView.as_view(), name='cancel_project'),
    path('<int:project_id>/similar/', SimilarProjectsView.as_view(), name='similar-projects'),
    path('Search/', SearchProjectsView.as_view(), name='project-search'),

]