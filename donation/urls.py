from django.urls import path
from donation.API.views import ProjectDonationView

urlpatterns = [
    path('api/projects/<int:project_id>/donate/', ProjectDonationView.as_view(), name='project-donation'),
]
