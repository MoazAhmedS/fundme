from django.db import models
from accounts.models import ProfileUser
from project.models import Project
from comments.models import Comment
# Create your models here.
class Report(models.Model):
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    report_details = models.TextField()
    report_date = models.DateField()

    def __str__(self):
        return f"Report {self.id} by {self.user.username}"

class ReportComment(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report {self.report.id} - Comment {self.comment.id}"


class ReportProject(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report {self.report.id} - Project {self.project.name}"

class Donation(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} donated {self.amount} to {self.project.name}"
