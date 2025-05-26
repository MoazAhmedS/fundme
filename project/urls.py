from django.urls import path
from project.api.views import ReadAndCreateProject
urlpatterns = [
    path('ReadOrCreate',ReadAndCreateProject.as_view(),name='read-or-create')
]