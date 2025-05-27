from django.urls import path
from .API.views import ReportCommentView, ReportProjectView

urlpatterns = [
    path('comments/<int:comment_id>/', ReportCommentView.as_view(), name='report-comment'),
    path('projects/<int:project_id>/', ReportProjectView.as_view(), name='report-project'),
]
