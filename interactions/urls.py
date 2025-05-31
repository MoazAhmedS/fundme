from django.urls import path
from .API.views import *

urlpatterns = [
    path('projects/<int:project_id>/rate/', RateCreateAPIView.as_view(), name='rate-project'),
    path('projects/rating/<int:project_id>/', RateListAPIView.as_view(), name='get-project-ratings'),
    path('tags/create/', CreateTagView.as_view()),
]
