from django.urls import path
from .API.views import *

urlpatterns = [
    path('API/projects/<int:project_id>/rate/', RateCreateAPIView.as_view(), name='rate-project'),
    path('API/projects/rating/<int:project_id>/', RateListAPIView.as_view(), name='get-project-ratings'),
]
